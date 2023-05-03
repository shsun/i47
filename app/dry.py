#!/usr/bin/python
# coding=utf-8
import pandas as pd

"""
每年分红3-5%

股息率（Dividend Yield Ratio）
"""


class DYRFilter(object):
    """

    """

    def __init__(self, ma_period1: int = 13, ma_period2: int = 21):
        self.MA_PERIOD1 = ma_period1
        self.MA_PERIOD2 = ma_period2
        super().__init__()

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
