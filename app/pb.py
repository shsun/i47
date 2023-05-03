#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
import pandas as pd

"""
PB<1
"""


class PBFilter(object):
    """

    """

    def __init__(self, p_data_frame: pd.DataFrame):
        super().__init__()
        self.data_frame = p_data_frame

    def doFilte(self) -> (bool, pd.DataFrame):
        success, df = None, None

        # pb_ratio                   float          市净率（该字段为比例字段，默认不展示%）

        # df = self.data_frame[self.data_frame.pb_ratio < 0]
        # print(df.sharp[0])
        # print(self.data_frame.sharp[0])

        self.data_frame = self.data_frame[self.data_frame['pb_ratio'] < 1]
        return success, self.data_frame
