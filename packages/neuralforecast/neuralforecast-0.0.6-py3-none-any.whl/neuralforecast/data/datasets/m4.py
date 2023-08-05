# AUTOGENERATED! DO NOT EDIT! File to edit: nbs/data_datasets__m4.ipynb (unless otherwise specified).

__all__ = ['Yearly', 'Quarterly', 'Monthly', 'Weekly', 'Daily', 'Hourly', 'Other', 'M4Info', 'M4', 'M4Evaluation']

# Cell
import os
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple, Union

import numpy as np
import pandas as pd

from .utils import download_file, Info
from ...losses.numpy import smape, mase

# Cell
@dataclass
class Yearly:
    seasonality: int = 1
    horizon: int = 6
    freq: str = 'Y'
    name: str = 'Yearly'
    n_ts: int = 23_000

@dataclass
class Quarterly:
    seasonality: int = 4
    horizon: int = 8
    freq: str = 'Q'
    name: str = 'Quarterly'
    n_ts: int = 24_000

@dataclass
class Monthly:
    seasonality: int = 12
    horizon: int = 18
    freq: str = 'M'
    name: str = 'Monthly'
    n_ts: int = 48_000

@dataclass
class Weekly:
    seasonality: int = 1
    horizon: int = 13
    freq: str = 'W'
    name: str = 'Weekly'
    n_ts: int = 359

@dataclass
class Daily:
    seasonality: int = 1
    horizon: int = 14
    freq: str = 'D'
    name: str = 'Daily'
    n_ts: int = 4_227

@dataclass
class Hourly:
    seasonality: int = 24
    horizon: int = 48
    freq: str = 'H'
    name: str = 'Hourly'
    n_ts: int = 414


@dataclass
class Other:
    seasonality: int = 1
    horizon: int = 8
    freq: str = 'D'
    name: str = 'Other'
    n_ts: int = 5_000
    included_groups: Tuple = ('Weekly', 'Daily', 'Hourly')

# Cell
M4Info = Info(groups=('Yearly', 'Quarterly', 'Monthly', 'Weekly', 'Daily', 'Hourly', 'Other'),
              class_groups=(Yearly, Quarterly, Monthly, Weekly, Daily, Hourly, Other))

# Cell
@dataclass
class M4:

    source_url: str = 'https://raw.githubusercontent.com/Mcompetitions/M4-methods/master/Dataset/'
    naive2_forecast_url: str = 'https://github.com/Nixtla/m4-forecasts/raw/master/forecasts/submission-Naive2.zip'

    @staticmethod
    def load(directory: str,
             group: str,
             cache: bool = True) -> Tuple[pd.DataFrame,
                                          Optional[pd.DataFrame],
                                          Optional[pd.DataFrame]]:
        """Downloads and loads M4 data.

        Parameters
        ----------
        directory: str
            Directory where data will be downloaded.
        group: str
            Group name.
            Allowed groups: 'Yearly', 'Quarterly', 'Monthly',
                            'Weekly', 'Daily', 'Hourly'.
        cache: bool
            If `True` saves and loads

        Notes
        -----
        [1] Returns train+test sets.
        """
        path = f'{directory}/m4/datasets'
        file_cache = f'{path}/{group}.p'

        if os.path.exists(file_cache) and cache:
            df, X_df, S_df = pd.read_pickle(file_cache)

            return df, X_df, S_df

        if group == 'Other':
            #Special case.
            included_dfs = [M4.load(directory, gr) \
                            for gr in M4Info['Other'].included_groups]
            df, *_ = zip(*included_dfs)
            df = pd.concat(df)
        else:
            M4.download(directory)
            path = f'{directory}/m4/datasets'
            class_group = M4Info[group]
            S_df = pd.read_csv(f'{directory}/m4/datasets/M4-info.csv',
                               usecols=['M4id','category'])
            S_df['category'] = S_df['category'].astype('category').cat.codes
            S_df.rename({'M4id': 'unique_id'}, axis=1, inplace=True)
            S_df = S_df[S_df['unique_id'].str.startswith(class_group.name[0])]

            def read_and_melt(file):
                df = pd.read_csv(file)
                df.columns = ['unique_id'] + list(range(1, df.shape[1]))
                df = pd.melt(df, id_vars=['unique_id'], var_name='ds', value_name='y')
                df = df.dropna()

                return df

            df_train = read_and_melt(file=f'{path}/{group}-train.csv')
            df_test = read_and_melt(file=f'{path}/{group}-test.csv')

            len_train = df_train.groupby('unique_id').agg({'ds': 'max'}).reset_index()
            len_train.columns = ['unique_id', 'len_serie']
            df_test = df_test.merge(len_train, on=['unique_id'])
            df_test['ds'] = df_test['ds'] + df_test['len_serie']
            df_test.drop('len_serie', axis=1, inplace=True)

            df = pd.concat([df_train, df_test])
            df = df.sort_values(['unique_id', 'ds']).reset_index(drop=True)

            S_df = S_df.sort_values('unique_id').reset_index(drop=True)

        X_df = None
        if cache:
            pd.to_pickle((df, X_df, S_df), file_cache)

        return df, None, S_df

    @staticmethod
    def download(directory: str) -> None:
        """Download M4 Dataset."""
        path = f'{directory}/m4/datasets/'
        if not os.path.exists(path):
            for group in M4Info.groups:
                download_file(path, f'{M4.source_url}/Train/{group}-train.csv')
                download_file(path, f'{M4.source_url}/Test/{group}-test.csv')
            download_file(path, f'{M4.source_url}/M4-info.csv')
            download_file(path, M4.naive2_forecast_url, decompress=True)

# Cell
class M4Evaluation:

    @staticmethod
    def load_benchmark(directory: str, group: str,
                       source_url: Optional[str] = None) -> np.ndarray:
        """Downloads and loads a bechmark forecasts.

        Parameters
        ----------
        directory: str
            Directory where data will be downloaded.
        group: str
            Group name.
            Allowed groups: 'Yearly', 'Quarterly', 'Monthly',
                            'Weekly', 'Daily', 'Hourly'.
        source_url: str, optional
            Optional benchmark url obtained from
            https://github.com/Nixtla/m4-forecasts/tree/master/forecasts.
            If `None` returns Naive2.

        Returns
        -------
        benchmark: numpy array
            Numpy array of shape (n_series, horizon).
        """
        path = f'{directory}/m4/datasets'
        initial = group[0]
        if source_url is not None:
            filename = source_url.split('/')[-1].replace('.rar', '.csv')
            filepath = f'{path}/{filename}'
            if not os.path.exists(filepath):
                download_file(path, source_url, decompress=True)

        else:
            filepath = f'{path}/submission-Naive2.csv'

        benchmark = pd.read_csv(filepath)
        benchmark = benchmark[benchmark['id'].str.startswith(initial)]
        benchmark = benchmark.set_index('id').dropna(1)
        benchmark = benchmark.sort_values('id').values

        return benchmark

    @staticmethod
    def evaluate(directory: str, group: str,
                 y_hat: Union[np.ndarray, str]) -> pd.DataFrame:
        """Evaluates y_hat according to M4 methodology.

        Parameters
        ----------
        directory: str
            Directory where data will be downloaded.
        group: str
            Group name.
            Allowed groups: 'Yearly', 'Quarterly', 'Monthly',
                            'Weekly', 'Daily', 'Hourly'.
        y_hat: numpy array, str
            Group forecasts as numpy array or
            benchmark url from
            https://github.com/Nixtla/m4-forecasts/tree/master/forecasts.

        Returns
        -------
        evaluation: pandas dataframe
            DataFrame with columns OWA, SMAPE, MASE
            and group as index.
        """
        if isinstance(y_hat, str):
            y_hat = M4Evaluation.load_benchmark(directory, group, y_hat)

        initial = group[0]
        class_group = M4Info[group]
        horizon = class_group.horizon
        seasonality = class_group.seasonality
        path = f'{directory}/m4/datasets'
        y_df, *_ = M4.load(directory, group)

        y_train = y_df.groupby('unique_id')['y']
        y_train = y_train.apply(lambda x: x.head(-horizon).values)
        y_train = y_train.values

        y_test = y_df.groupby('unique_id')['y']
        y_test = y_test.tail(horizon)
        y_test = y_test.values.reshape(-1, horizon)

        naive2 = M4Evaluation.load_benchmark(directory, group)
        smape_y_hat = smape(y_test, y_hat)
        smape_naive2 = smape(y_test, naive2)

        mase_y_hat = np.mean([mase(y_test[i], y_hat[i], y_train[i], seasonality)
                              for i in range(class_group.n_ts)])
        mase_naive2 = np.mean([mase(y_test[i], naive2[i], y_train[i], seasonality)
                               for i in range(class_group.n_ts)])

        owa = .5 * (mase_y_hat / mase_naive2 + smape_y_hat / smape_naive2)

        evaluation = pd.DataFrame({'SMAPE': smape_y_hat,
                                   'MASE': mase_y_hat,
                                   'OWA': owa},
                                   index=[group])

        return evaluation