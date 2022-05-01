from datetime import date, timedelta, datetime

import pandas as pd
from . import models
from dpf.lib.db import engine


def register_subparsers(parser):
    last_week = (date.today() - timedelta(10) - timedelta(3)).strftime('%Y-%m-%d')

    subparsers = parser.add_subparsers(required=True)
    update_db_parser = subparsers.add_parser('update-db')
    update_db_parser.add_argument('--start', required=False, default=last_week)
    update_db_parser.set_defaults(func=update_db_cmd)


def update_db_cmd(args):
    start = datetime.strptime(args.start, '%Y-%m-%d')
    data = get_latest_data(start)

    data.to_sql(models.Cases.__tablename__, engine, if_exists='replace')


def get_latest_data(start_date: date) -> pd.DataFrame:
    sidep_data: pd.DataFrame = pd.read_csv(
        'https://www.data.gouv.fr/fr/datasets/r/dd0de5d9-b5a5-4503-930a-7b08dc0adc7c',
        parse_dates=True,
        index_col="jour",
        usecols=["jour", "P", "cl_age90", 'T', 'pop'],
        sep=';'
    )
    end_date = date.today()

    everyone_data = sidep_data.loc[sidep_data.loc[:, 'cl_age90'] == 0].copy()

    p = everyone_data.loc[:, 'P'].copy()
    t = everyone_data.loc[:, 'T'].copy()
    r: pd.DataFrame = 100 * p / t
    everyone_data.loc[:, 'Ratio'] = r.round(decimals=1)
    everyone_data.loc[:, 'P'] = (p / 1000).round(decimals=1)
    everyone_data.loc[:, 'T'] = (t / 1000).round(decimals=1)
    rolling_mean = (
            p.rolling(min_periods=1, window=7).mean() / 1000
    ).round(decimals=1).astype(int)
    everyone_data.loc[:, 'Mean'] = rolling_mean

    rolling_rate = (
        r.rolling(min_periods=1, window=7).mean().round(decimals=1)
    )
    everyone_data.loc[:, 'RollingRate'] = rolling_rate

    rolling_tests = (
        (t / 1000).rolling(min_periods=1, window=7).mean().round(decimals=1)
    )
    everyone_data.loc[:, 'RollingTests'] = rolling_tests

    latest_data = everyone_data.loc[start_date:end_date].copy()
    latest_data = latest_data.drop(['cl_age90'], axis=1)
    latest_data = latest_data.drop(['pop'], axis=1)
    latest_data = latest_data.rename_axis(
        "Date",
        axis='rows'
    )

    return latest_data.reindex(index=latest_data.index[::-1])
