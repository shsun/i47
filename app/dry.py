#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
import pandas as pd

"""
每年分红3-5%

股息率（Dividend Yield Ratio），是一年的总派息额与当时市价的比例。以占股票最后销售价格的百分数表示的年度股息，该指标是投资收益率的简化形式。
股息率是股息与股票价格之间的比率。
"""


class DYRFilter(object):
    """

    """

    def __init__(self, p_data_frame: pd.DataFrame, p_start_datetime: datetime = None, p_end_datetime: datetime = None):
        super().__init__()

        self.start_datetime = p_start_datetime
        self.end_datetime = p_end_datetime
        self.data_frame = p_data_frame

    def doFilte(self, input_data: pd.DataFrame, info_data: dict) -> (bool, pd.DataFrame):
        """
        :param input_data: Yahoo Finance Quantitative Data (Price, Volume, etc.)
        :param info_data: Yahoo Finance Fundamental Data (Company Description. PE Ratio, Etc.)
        :return:
        """
        if input_data.empty or input_data.shape[0] < 21:
            return False

        input_data['MA_1'] = input_data['close'].rolling(window=self.MA_PERIOD1).mean()
        input_data['MA_2'] = input_data['close'].rolling(window=self.MA_PERIOD2).mean()

        current_record = input_data.iloc[-1]
        return True if (current_record['close'] > current_record['MA_1'] and current_record['close'] > current_record[
            'MA_2']) else False
