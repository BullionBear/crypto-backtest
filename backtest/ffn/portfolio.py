import numpy as np
import pandas as pd
from .const import *

"""
portfolio.py collect all common calculation base on a pd.DataFrame input
The calculation usually require some information:
1. NAV
2. NAV timestamp in ms: int
3. rescale (Optional): str, usually represent as 1s, 5m,..., 3d
"""


def calc_return(df: pd.DataFrame, nav_col: str):
    return (df[nav_col][len(df) - 1] - df[nav_col][0]) / df[nav_col][0]


def calc_interval_return(df: pd.DataFrame, ts_col: str, nav_col: str, interval: str):
    r = (df[nav_col][len(df) - 1] - df[nav_col][0]) / df[nav_col][0]
    span = df[ts_col][len(df) - 1] - df[ts_col][0]
    interval_in_ms = convert_to_milliseconds(interval)
    return r * interval_in_ms / span


def calc_interval_volatility(df: pd.DataFrame, ts_col: str, nav_col: str, interval: str):
    df = df.copy()
    df["log_return"] = np.log(df[nav_col] / df[nav_col].shift(1))
    df['diff'] = df[ts_col].diff()
    df = df.dropna()
    r = np.sum(df['log_return'] * df['diff']) / np.sum(df['diff'])
    df['diff_sq'] = np.power(df["diff"], 2)
    var = (np.power(df["log_return"] - r, 2) * df['diff_sq']).sum() / df['diff_sq'].sum()
    volatility = np.sqrt(var)
    ave_span = df['diff'].mean()
    interval_in_ms = convert_to_milliseconds(interval)
    volatility = volatility * np.sqrt(interval_in_ms / ave_span)
    return volatility


def calc_mdd(df: pd.DataFrame, nav_col: str):
    cumulative_max = df[nav_col].cummax()
    drawdown = cumulative_max - df[nav_col]
    drawdown_percentage = drawdown / cumulative_max
    max_drawdown = drawdown_percentage.max()
    return max_drawdown


def calc_interval_sharpe_ratio(df: pd.DataFrame, ts_col: str, nav_col: str, interval: str):
    r = calc_interval_volatility(df, ts_col, nav_col, interval)
    volatility = calc_interval_volatility(df, ts_col, nav_col, interval)
    return r / volatility


def convert_to_milliseconds(time: str):
    units = {
        's': SECOND_IN_MS,
        'm': MINUTE_IN_MS,
        'h': HOUR_IN_MS,
        'd': DAY_IN_MS,
    }

    unit = time[-1]
    number = int(time[:-1])

    return number * units[unit]
