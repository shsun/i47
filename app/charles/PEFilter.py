#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
import pandas as pd

"""
PE<10
"""


class PEFilter(object):
    """

    """

    def __init__(self, p_data_frame: pd.DataFrame):
        super().__init__()
        self.data_frame = p_data_frame

    def doFilte(self) -> (bool, pd.DataFrame):
        success, df = None, None
        self.data_frame = self.data_frame[self.data_frame['pe_ratio'] < 10]
        return success, self.data_frame
