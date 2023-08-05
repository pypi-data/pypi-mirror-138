# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/data__tsdataset.ipynb (unless otherwise specified).

__all__ = ['BaseDataset', 'get_default_mask_df', 'TimeSeriesDataset', 'IterateWindowsDataset', 'WindowsDataset']

# Cell
import gc
import logging
from typing import Dict, List, Optional, Tuple, Union
from typing_extensions import Literal

import numpy as np
import pandas as pd
import torch as t
from fastcore.foundation import patch
from torch.utils.data import Dataset

# Cell
class BaseDataset(Dataset):
    """
    A class used to store Time Series data.
    """

    def __init__(self,
                 Y_df: pd.DataFrame,
                 X_df: Optional[pd.DataFrame] = None,
                 S_df: Optional[pd.DataFrame] = None,
                 f_cols: Optional[List] = None,
                 mask_df: Optional[pd.DataFrame] = None,
                 ds_in_test: int = 0,
                 is_test: bool = False,
                 input_size: int = None,
                 output_size: int = None,
                 complete_windows: bool = True,
                 verbose: bool = False) -> 'BaseDataset':
        """
        Parameters
        ----------
        Y_df: pd.DataFrame
            Target time series with columns ['unique_id', 'ds', 'y'].
        X_df: pd.DataFrame
            Exogenous time series with columns ['unique_id', 'ds', 'y'].
        S_df: pd.DataFrame
            Static exogenous variables with columns ['unique_id', 'ds']
            and static variables.
        f_cols: list
            List of exogenous variables of the future.
        mask_df: pd.DataFrame
            Outsample mask with columns ['unique_id', 'ds', 'sample_mask']
            and optionally 'available_mask'.
            Default None: constructs default mask based on ds_in_test.
        ds_in_test: int
            Only used when mask_df = None.
            Numer of datestamps to use as outsample.
        is_test: bool
            Only used when mask_df = None.
            Wheter target time series belongs to test set.
        input_size: int
            Size of the training sets.
        output_size: int
            Forecast horizon.
        complete_windows: bool
            Whether consider only windows with sample_mask equal to output_size.
            Default False.
        verbose: bool
            Wheter or not log outputs.
        """
        assert type(Y_df) == pd.core.frame.DataFrame
        assert all([(col in Y_df) for col in ['unique_id', 'ds', 'y']])
        self.verbose = verbose

        if X_df is not None:
            assert type(X_df) == pd.core.frame.DataFrame
            assert all([(col in X_df) for col in ['unique_id', 'ds']])
            assert len(Y_df)==len(X_df), 'The dimensions of Y_df and X_df are not the same'

        if mask_df is not None:
            assert len(Y_df)==len(mask_df), 'The dimensions of Y_df and mask_df are not the same'
            assert all([(col in mask_df) for col in ['unique_id', 'ds', 'sample_mask']])
            if 'available_mask' not in mask_df.columns:
                if self.verbose:
                    logging.info('Available mask not provided, defaulted with 1s.')
                mask_df['available_mask'] = 1
            assert np.sum(np.isnan(mask_df.available_mask.values)) == 0
            assert np.sum(np.isnan(mask_df.sample_mask.values)) == 0
        else:
            mask_df = get_default_mask_df(Y_df=Y_df,
                                          is_test=is_test,
                                          ds_in_test=ds_in_test)

        n_ds  = len(mask_df)
        n_avl = mask_df.available_mask.sum()
        n_ins = mask_df.sample_mask.sum()
        n_out = len(mask_df) - mask_df.sample_mask.sum()

        avl_prc = np.round((100 * n_avl) / n_ds, 2)
        ins_prc = np.round((100 * n_ins) / n_ds, 2)
        out_prc = np.round((100 * n_out) / n_ds, 2)
        if self.verbose:
            logging.info('Train Validation splits\n')
            if len(mask_df.unique_id.unique()) < 10:
                logging.info(mask_df.groupby(['unique_id', 'sample_mask']).agg({'ds': ['min', 'max']}))
            else:
                logging.info(mask_df.groupby(['sample_mask']).agg({'ds': ['min', 'max']}))
            dataset_info  = f'\nTotal data \t\t\t{n_ds} time stamps \n'
            dataset_info += f'Available percentage={avl_prc}, \t{n_avl} time stamps \n'
            dataset_info += f'Insample  percentage={ins_prc}, \t{n_ins} time stamps \n'
            dataset_info += f'Outsample percentage={out_prc}, \t{n_out} time stamps \n'
            logging.info(dataset_info)

        self.ts_data, self.s_matrix, self.meta_data, self.t_cols, self.s_cols \
                         = self._df_to_lists(Y_df=Y_df, S_df=S_df, X_df=X_df, mask_df=mask_df)

        # Dataset attributes
        self.n_series = len(self.ts_data)
        self.max_len = max([len(ts) for ts in self.ts_data])
        self.n_channels = len(self.t_cols) # t_cols insample_mask and outsample_mask
        self.frequency = pd.infer_freq(Y_df.head()['ds'])
        self.f_cols = f_cols
        self.f_idxs = self._get_f_idxs(f_cols) if f_cols else []
        self.input_size = input_size
        self.output_size = output_size
        self.complete_windows = complete_windows
        self.first_ds = 0

        # Number of X and S features
        self.n_x = 0 if X_df is None else X_df.shape[1] - 2 # -2 for unique_id and ds
        self.n_s = 0 if S_df is None else S_df.shape[1] - 1 # -1 for unique_id

        # Balances panel and creates
        # numpy  s_matrix of shape (n_series, n_s)
        # numpy ts_tensor of shape (n_series, n_channels, max_len) n_channels = t_cols + masks
        self.len_series, self.ts_tensor = self._create_tensor()

        # Defining sampleable time series
        self.ts_idxs = np.arange(self.n_series)
        self.sampleable_ts_idxs: np.ndarray
        self.n_sampleable_ts: int

        self._define_sampleable_ts_idxs()

# Cell
@patch
def _define_sampleable_ts_idxs(self: BaseDataset):
    self.n_sampleable_ts = len(self.ts_tensor)
    self.sampleable_ts_idxs = self.ts_idxs.copy()

# Cell
@patch
def _df_to_lists(self: BaseDataset,
                 S_df: pd.DataFrame,
                 Y_df: pd.DataFrame,
                 X_df: pd.DataFrame,
                 mask_df: pd.DataFrame) -> Tuple[List[np.ndarray],
                                                 List[np.ndarray],
                                                 List[np.ndarray],
                                                 List[str],
                                                 List[str]]:
    """Transforms input dataframes to lists.

    Parameters
    ----------
    S_df: pd.DataFrame
        Static exogenous variables with columns ['unique_id', 'ds']
        and static variables.
    Y_df: pd.DataFrame
        Target time series with columns ['unique_id', 'ds', 'y'].
    X_df: pd.DataFrame
        Exogenous time series with columns ['unique_id', 'ds', 'y'].
    mask_df: pd.DataFrame
        Outsample mask with columns ['unique_id', 'ds', 'sample_mask']
        and optionally 'available_mask'.
        Default None: constructs default mask based on ds_in_test.

    Returns
    -------
    Tuple of five lists:
        - List of time series. Each element of the list is a
          numpy array of shape (length of the time series, n_channels),
          where n_channels = t_cols + masks.
        - List of static variables. Each element of the list is a
          numpy array of shape (1, n_s).
          where n_channels = t_cols + masks.
        - List of meta data. Each element of the list is a
          numpy array of shape (lenght of the time series, 2)
          and corresponds to unique_id, ds.
        - List of temporal variables (including target and masks).
        - List of statitc variables.
    """
    # None protections
    if X_df is None:
        X_df = Y_df[['unique_id', 'ds']]

    if S_df is None:
        S_df = Y_df[['unique_id']].drop_duplicates()

    # Protect order of data
    Y = Y_df.sort_values(by=['unique_id', 'ds'], ignore_index=True).copy()
    X = X_df.sort_values(by=['unique_id', 'ds'], ignore_index=True).copy()
    M = mask_df.sort_values(by=['unique_id', 'ds'], ignore_index=True).copy()

    assert np.array_equal(X.unique_id.values, Y.unique_id.values), f'Mismatch in X, Y unique_ids'
    assert np.array_equal(X.ds.values, Y.ds.values), f'Mismatch in X, Y ds'
    assert np.array_equal(M.unique_id.values, Y.unique_id.values), f'Mismatch in M, Y unique_ids'
    assert np.array_equal(M.ds.values, Y.ds.values), f'Mismatch in M, Y ds'

    # Create bigger grouped by dataframe G to parse
    M = M[['available_mask', 'sample_mask']]
    X.drop(['unique_id', 'ds'], 1, inplace=True)
    G = Y.join(X).join(M)

    S = S_df.sort_values('unique_id')

    # time columns and static columns for future indexing
    t_cols = list(G.columns[2:]) # avoid unique_id and ds
    s_cols = list(S.columns[1:]) # avoid unique_id

    grouped = G.groupby('unique_id')
    meta = G[['unique_id', 'ds']].values
    data = G.drop(columns=['unique_id', 'ds']).values
    sizes = grouped.size()
    idxs = np.append(0, sizes.cumsum())
    ts_data = []
    meta_data = []
    for start, end in zip(idxs[:-1], idxs[1:]):
        ts_data.append(data[start:end])
        meta_data.append(meta[start:end])

    if S['unique_id'].value_counts().max() > 1:
        raise ValueError('Found duplicated unique_ids in S_df')
    s_data = S.drop(columns='unique_id').values

    del S, Y, X, M, G
    gc.collect()

    return ts_data, s_data, meta_data, t_cols, s_cols

# Cell
@patch
def _create_tensor(self: BaseDataset) -> Tuple[np.array, t.Tensor]:
    """Transforms outputs from self._df_to_lists to numpy arrays."""
    ts_tensor = np.zeros((self.n_series, self.n_channels, self.max_len))

    len_series = np.empty(self.n_series, dtype=np.int32)
    for idx, ts_idx in enumerate(self.ts_data):
        # Left padded time series tensor
        ts_tensor[idx, :, -ts_idx.shape[0]:] = ts_idx.T
        len_series[idx] = ts_idx.shape[0]

    ts_tensor = t.Tensor(ts_tensor)

    return len_series, ts_tensor

# Cell
@patch
def _get_f_idxs(self: BaseDataset,
               cols: List[str]) -> List:
    """Gets indexes of exogenous variables.

    Parameters
    ----------
    cols: List[str]
        Interest exogenous variables.

    Returns
    -------
    Indexes of cols variables.
    """
    # Check if cols are available f_cols and return the idxs
    if not all(col in self.f_cols for col in cols):
        str_cols = ', '.join(cols)
        raise Exception(f'Some variables in {str_cols} are not available in f_cols.')

    f_idxs = [self.t_cols.index(col) for col in cols]

    return f_idxs

# Cell
@patch
def __getitem__(self: BaseDataset,
                idx: Union[slice, int]) -> Dict[str, t.Tensor]:
    """Creates batch based on index.

    Parameters
    ----------
    index: np.ndarray
        Indexes of time series to consider.

    Returns
    -------
    Dictionary with keys:
        - S
        - Y
        - X
        - available_mask
        - sample_mask
        - idxs
    """
    # Checks for idx
    pass

# Cell
@patch
def __len__(self: BaseDataset):
    return self.n_series

# Cell
@patch
def get_n_variables(self: BaseDataset) -> Tuple[int, int]:
    """Gets number of exogenous and static variables."""
    return self.n_x, self.n_s

@patch
def get_n_series(self: BaseDataset) -> int:
    """Gets number of time series."""
    return self.n_series

@patch
def get_max_len(self: BaseDataset) -> int:
    """Gets max len of time series."""
    return self.max_len

@patch
def get_n_channels(self: BaseDataset) -> int:
    """Gets number of channels considered."""
    return self.n_channels

@patch
def get_frequency(self: BaseDataset) -> str:
    """Gets infered frequency."""
    return self.frequency

# Cell
def get_default_mask_df(Y_df: pd.DataFrame,
                        ds_in_test: int,
                        is_test: bool) -> pd.DataFrame:
    """Constructs default mask df.

    Parameters
    ----------
    Y_df: pd.DataFrame
        Target time series with columns ['unique_id', 'ds', 'y'].
    ds_in_test: int
        Numer of datestamps to use as outsample.
    is_test: bool
        Wheter target time series belongs to test set.

    Returns
    -------
    Mask DataFrame with columns
    ['unique_id', 'ds', 'available_mask', 'sample_mask'].
    """
    mask_df = Y_df[['unique_id', 'ds']].copy()
    mask_df['available_mask'] = 1
    mask_df['sample_mask'] = 1
    mask_df = mask_df.set_index(['unique_id', 'ds'])

    mask_df_s = mask_df.sort_values(by=['unique_id', 'ds'])
    zero_idx = mask_df_s.groupby('unique_id').tail(ds_in_test).index
    mask_df.loc[zero_idx, 'sample_mask'] = 0
    mask_df = mask_df.reset_index()
    mask_df.index = Y_df.index

    assert len(mask_df)==len(Y_df), \
        f'The mask_df length {len(mask_df)} is not equal to Y_df length {len(Y_df)}'

    if is_test:
        mask_df['sample_mask'] = 1 - mask_df['sample_mask']

    return mask_df

# Cell
class TimeSeriesDataset(BaseDataset):
    """
    A class used to store Time Series data.
    Each element is a windows index.
    Returns a windows for all time series.
    """

    def __init__(self,
                 Y_df: pd.DataFrame,
                 input_size: int,
                 output_size: int,
                 X_df: Optional[pd.DataFrame] = None,
                 S_df: Optional[pd.DataFrame] = None,
                 f_cols: Optional[List] = None,
                 mask_df: Optional[pd.DataFrame] = None,
                 ds_in_test: int = 0,
                 is_test: bool = False,
                 complete_windows: bool = True,
                 verbose: bool = False) -> 'TimeSeriesDataset':
        """
        Parameters
        ----------
        Y_df: pd.DataFrame
            Target time series with columns ['unique_id', 'ds', 'y'].
        input_size: int
            Size of the training sets.
        output_size: int
            Forecast horizon.
        X_df: pd.DataFrame
            Exogenous time series with columns ['unique_id', 'ds', 'y'].
        S_df: pd.DataFrame
            Static exogenous variables with columns ['unique_id', 'ds']
            and static variables.
        f_cols: list
            List of exogenous variables of the future.
        mask_df: pd.DataFrame
            Outsample mask with columns ['unique_id', 'ds', 'sample_mask']
            and optionally 'available_mask'.
            Default None: constructs default mask based on ds_in_test.
        ds_in_test: int
            Only used when mask_df = None.
            Numer of datestamps to use as outsample.
        is_test: bool
            Only used when mask_df = None.
            Wheter target time series belongs to test set.
        verbose: bool
            Wheter or not log outputs.
        """
        super(TimeSeriesDataset, self).__init__(Y_df=Y_df, input_size=input_size,
                                                output_size=output_size,
                                                X_df=X_df, S_df=S_df, f_cols=f_cols,
                                                mask_df=mask_df, ds_in_test=ds_in_test,
                                                is_test=is_test, complete_windows=complete_windows,
                                                verbose=verbose)

# Cell
@patch
def __getitem__(self: TimeSeriesDataset,
                idx: Union[slice, int]) -> Dict[str, t.Tensor]:
    """Creates batch based on index.

    Parameters
    ----------
    index: np.ndarray
        Indexes of time series to consider.

    Returns
    -------
    Dictionary with keys:
        - S
        - Y
        - X
        - available_mask
        - sample_mask
        - idxs
    """
    # Checks for idx
    if isinstance(idx, int):
        idx = [idx]
    elif isinstance(idx, slice) or isinstance(idx, list):
        pass
    else:
        raise Exception('Use slices, int or list for getitem.')

    # Parse windows to elements of batch
    S = t.Tensor(self.s_matrix[idx])
    Y = self.ts_tensor[idx, self.t_cols.index('y'), :]
    X = self.ts_tensor[idx, (self.t_cols.index('y') + 1):self.t_cols.index('available_mask'), :]

    available_mask = self.ts_tensor[idx, self.t_cols.index('available_mask'), :]
    sample_mask = self.ts_tensor[idx, self.t_cols.index('sample_mask'), :]
    ts_idxs = t.as_tensor(idx, dtype=t.long)

    batch = {'S': S, 'Y': Y, 'X': X,
             'available_mask': available_mask,
             'sample_mask': sample_mask,
             'idxs': ts_idxs}

    return batch

# Cell
class IterateWindowsDataset(BaseDataset):
    """
    A class used to store Time Series data.
    """

    def __init__(self,
                 Y_df: pd.DataFrame,
                 input_size: int,
                 output_size: int,
                 X_df: Optional[pd.DataFrame] = None,
                 S_df: Optional[pd.DataFrame] = None,
                 f_cols: Optional[List] = None,
                 mask_df: Optional[pd.DataFrame] = None,
                 ds_in_test: int = 0,
                 is_test: bool = False,
                 verbose: bool = False) -> 'IterateWindowsDataset':
        """
        Parameters
        ----------
        Y_df: pd.DataFrame
            Target time series with columns ['unique_id', 'ds', 'y'].
        input_size: int
            Size of the training sets.
        output_size: int
            Forecast horizon.
        X_df: pd.DataFrame
            Exogenous time series with columns ['unique_id', 'ds', 'y'].
        S_df: pd.DataFrame
            Static exogenous variables with columns ['unique_id', 'ds']
            and static variables.
        f_cols: list
            List of exogenous variables of the future.
        mask_df: pd.DataFrame
            Outsample mask with columns ['unique_id', 'ds', 'sample_mask']
            and optionally 'available_mask'.
            Default None: constructs default mask based on ds_in_test.
        ds_in_test: int
            Only used when mask_df = None.
            Numer of datestamps to use as outsample.
        is_test: bool
            Only used when mask_df = None.
            Wheter target time series belongs to test set.
        verbose: bool
            Wheter or not log outputs.
        """
        super(IterateWindowsDataset, self).__init__(Y_df=Y_df, input_size=input_size,
                                                    output_size=output_size,
                                                    X_df=X_df, S_df=S_df, f_cols=f_cols,
                                                    mask_df=mask_df, ds_in_test=ds_in_test,
                                                    is_test=is_test, complete_windows=True,
                                                    verbose=verbose)

        self.first_sampleable_stamps = np.nonzero(self.ts_tensor[0, self.t_cols.index('sample_mask'), :])[0,0]
        self.sampleable_stamps = t.sum(self.ts_tensor[0, self.t_cols.index('sample_mask'), :]) # TODO: now it assumes mask is correct

        self.first_sampleable_stamps = int(self.first_sampleable_stamps.cpu().detach().numpy())
        self.sampleable_stamps = int(self.sampleable_stamps.cpu().detach().numpy())

# Cell
@patch
def __getitem__(self: IterateWindowsDataset,
                idx: int) -> Dict[str, t.Tensor]:
    """Creates batch based on index.

    Parameters
    ----------
    idx:
        Index of windowß to consider.

    Returns
    -------
    Dictionary with keys:
        - S
        - Y
        - X
        - available_mask
        - sample_mask
        - idxs
    """
    # Checks for idx
    if not isinstance(idx, int):
        raise Exception('idx should be an integer')

    # Add first sampleable stamp and shift by input_size if possible (this will never happen during training)
    if self.first_sampleable_stamps + 1 > self.input_size:
        idx = idx + self.first_sampleable_stamps - self.input_size

    # Parse windows to elements of batch
    end = idx + self.input_size + self.output_size
    S = t.Tensor(self.s_matrix)
    Y = self.ts_tensor[:, self.t_cols.index('y'), idx:end]
    X = self.ts_tensor[:, (self.t_cols.index('y') + 1):self.t_cols.index('available_mask'), idx:end]

    available_mask = self.ts_tensor[:, self.t_cols.index('available_mask'), idx:end]
    sample_mask = self.ts_tensor[:, self.t_cols.index('sample_mask'), idx:end]
    ts_idxs = t.as_tensor(np.arange(self.n_series), dtype=t.long)

    batch = {'S': S, 'Y': Y, 'X': X,
             'available_mask': available_mask,
             'sample_mask': sample_mask,
             'idxs': ts_idxs}

    return batch

# Cell
@patch
def __len__(self: IterateWindowsDataset):
    if self.first_sampleable_stamps + 1 > self.input_size:
        return self.sampleable_stamps - self.output_size + 1 # We take the input_size chunk from the beginning, if possible
    else:
        return self.sampleable_stamps - self.input_size - self.output_size + 1

# Cell
class WindowsDataset(BaseDataset):
    """
    A class used to store Time Series data.
    """

    def __init__(self,
                 Y_df: pd.DataFrame,
                 input_size: int,
                 output_size: int,
                 X_df: Optional[pd.DataFrame] = None,
                 S_df: Optional[pd.DataFrame] = None,
                 f_cols: Optional[List] = None,
                 mask_df: Optional[pd.DataFrame] = None,
                 ds_in_test: int = 0,
                 is_test: bool = False,
                 sample_freq: int = 1,
                 complete_windows: bool = False,
                 last_window: bool = False,
                 verbose: bool = False) -> 'TimeSeriesDataset':
        """
        Parameters
        ----------
        Y_df: pd.DataFrame
            Target time series with columns ['unique_id', 'ds', 'y'].
        input_size: int
            Size of the training sets.
        output_size: int
            Forecast horizon.
        X_df: pd.DataFrame
            Exogenous time series with columns ['unique_id', 'ds', 'y'].
        S_df: pd.DataFrame
            Static exogenous variables with columns ['unique_id', 'ds']
            and static variables.
        f_cols: list
            List of exogenous variables of the future.
        mask_df: pd.DataFrame
            Outsample mask with columns ['unique_id', 'ds', 'sample_mask']
            and optionally 'available_mask'.
            Default None: constructs default mask based on ds_in_test.
        ds_in_test: int
            Only used when mask_df = None.
            Numer of datestamps to use as outsample.
        is_test: bool
            Only used when mask_df = None.
            Wheter target time series belongs to test set.
        last_window: bool
            Only used for forecast (test)
            Wheter the dataset will include only last window for each time serie.
        verbose: bool
            Wheter or not log outputs.
        """
        super(WindowsDataset, self).__init__(Y_df=Y_df, input_size=input_size,
                                             output_size=output_size,
                                             X_df=X_df, S_df=S_df, f_cols=f_cols,
                                             mask_df=mask_df, ds_in_test=ds_in_test,
                                             is_test=is_test, complete_windows=complete_windows,
                                             verbose=verbose)
        # WindowsDataset parameters
        self.windows_size = self.input_size + self.output_size
        self.padding = (self.input_size, self.output_size)
        self.sample_freq = sample_freq
        self.last_window = last_window
        self.device = 'cuda' if t.cuda.is_available() else 'cpu'

# Cell
@patch
def _create_windows_tensor(self: WindowsDataset,
                           idx: slice) -> Tuple[t.Tensor, t.Tensor, t.Tensor]:
    """Creates windows of size windows_size from
    the ts_tensor of the TimeSeriesDataset filtered by
    window_sampling_limit and ts_idxs. The step of each window
    is defined by idx_to_sample_freq.

    Parameters
    ----------
    index: slice
        Indexes of time series to consider.

    Returns
    -------
    Tuple of three elements:
        - Windows tensor of shape (windows, channels, input_size + output_size)
        - Static variables tensor of shape (windows * series, n_static)
        - Time Series indexes for each window.
    """
    # Default ts_idxs=ts_idxs sends all the data, otherwise filters series
    tensor = self.ts_tensor[idx, :, self.first_ds:]

    padder = t.nn.ConstantPad1d(padding=self.padding, value=0)
    tensor = padder(tensor)

    # Creating rolling windows and 'flattens' them
    tensor = tensor.to(self.device)
    windows = tensor.unfold(dimension=-1,
                            size=self.windows_size,
                            step=self.sample_freq)
    # n_serie, n_channel, n_time, window_size -> n_serie, n_time, n_channel, window_size
    windows = windows.permute(0, 2, 1, 3)
    windows = windows.reshape(-1, self.n_channels, self.windows_size)

    # Broadcast s_matrix: This works because unfold in windows_tensor, orders: serie, time

    ts_idxs = self.ts_idxs[idx]
    n_ts = len(ts_idxs)
    windows_per_serie = len(windows) / n_ts

    ts_idxs = ts_idxs.repeat(repeats=windows_per_serie)
    s_matrix = self.s_matrix[idx]
    s_matrix = s_matrix.repeat(repeats=windows_per_serie, axis=0)

    s_matrix = t.Tensor(s_matrix)
    ts_idxs = t.as_tensor(ts_idxs, dtype=t.long)

    windows_idxs = self._get_sampleable_windows_idxs(ts_windows_flatten=windows,
                                                     ts_idxs=ts_idxs)

    # Raise error if nothing to sample from
    if not windows_idxs.size:
        raise Exception(
            f'Time Series {idx} are not sampleable. '
            'Check the data, masks, window_sampling_limit, '
            'input_size, output_size, masks.'
        )

    # Index the windows and s_matrix tensors of batch
    windows = windows[windows_idxs]
    s_matrix = s_matrix[windows_idxs]
    ts_idxs = ts_idxs[windows_idxs]

    return windows, s_matrix, ts_idxs

# Cell
@patch
#TODO: do we want complete? inputs seems irrelevant, NBEATS dont use it, for now is our only model
def _get_sampleable_windows_idxs(self: WindowsDataset,
                                 ts_windows_flatten: t.Tensor,
                                 ts_idxs: t.Tensor) -> np.ndarray:
    """Gets indexes of windows that fulfills conditions.

    Parameters
    ----------
    ts_windows_flatten: t.Tensor
        Tensor of shape (windows, n_channels, windows_size)

    Returns
    -------
    Numpy array of indexes of ts_windows_flatten that
    fulfills conditions.

    Notes
    -----
    """

    if self.last_window:
        _, idxs_counts = t.unique(ts_idxs, return_counts=True)
        last_idxs = idxs_counts.cumsum(0) - 1
        last_idxs = last_idxs.numpy()

        return last_idxs

    if self.complete_windows:
        sample_condition = ts_windows_flatten[:, self.t_cols.index('sample_mask'), -(self.output_size):]
        sample_condition = (sample_condition > 0) * 1 # Converts continuous sample_mask (with weights) to 0-1
        sample_condition = t.sum(sample_condition, axis=1)
        sample_condition = (sample_condition == self.output_size) * 1

    else:
        sample_condition = ts_windows_flatten[:, self.t_cols.index('sample_mask'), -self.output_size:]
        sample_condition = (sample_condition > 0) * 1 # Converts continuous sample_mask (with weights) to 0-1
        sample_condition = t.sum(sample_condition, axis=1)
        sample_condition = (sample_condition > 0) * 1

    sampling_idx = t.nonzero(sample_condition > 0)
    sampling_idx = sampling_idx.cpu().detach().numpy()
    sampling_idx = sampling_idx.flatten()

    return sampling_idx

# Cell
@patch
def __getitem__(self: WindowsDataset,
                idx: Union[slice, int]) -> Dict[str, t.Tensor]:
    """Creates batch based on index.

    Parameters
    ----------
    index: np.ndarray
        Indexes of time series to consider.

    Returns
    -------
    Dictionary with keys:
        - S
        - Y
        - X
        - available_mask
        - sample_mask
        - idxs
    """
    # Checks for idx
    if isinstance(idx, int):
        idx = [idx]
    elif isinstance(idx, slice) or isinstance(idx, list):
        pass
    else:
        raise Exception('Use slices, int or list for getitem.')

    # Create windows for each sampled ts and sample random unmasked windows from each ts
    windows, S, ts_idxs = self._create_windows_tensor(idx=idx)

    # Parse windows to elements of batch
    Y = windows[:, self.t_cols.index('y'), :]
    X = windows[:, (self.t_cols.index('y') + 1):self.t_cols.index('available_mask'), :]
    available_mask = windows[:, self.t_cols.index('available_mask'), :]
    sample_mask = windows[:, self.t_cols.index('sample_mask'), :]

    batch = {'S': S, 'Y': Y, 'X': X,
             'available_mask': available_mask,
             'sample_mask': sample_mask,
             'idxs': ts_idxs}

    return batch