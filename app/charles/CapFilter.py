#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
import pandas as pd

"""
大市值股票（通常市值大于100亿/600亿?）应占到仓位的70%。

total_market_val	float	总市值
circular_market_val	float	流通市值
"""


class CapFilter(object):
    """

    """

    def __init__(self, p_data_frame: pd.DataFrame):
        super().__init__()
        self.data_frame = p_data_frame

    def doFilte(self) -> (bool, pd.DataFrame):
        success, df = None, None
        self.data_frame = self.data_frame[self.data_frame['total_market_val'] > 600 * 100000000]
        return success, self.data_frame
