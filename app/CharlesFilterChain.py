#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
import pandas as pd


class CharlesFilterChain(object):
    """

    """

    def __init__(self, p_data_frame: pd.DataFrame):
        super().__init__()
        self.data_frame = p_data_frame
        self.filters = list()

    def add_filter(self, p_filter=None):
        self.filters.append(p_filter)

    def doFilte(self) -> (bool, pd.DataFrame):
        for i, v in enumerate(self.filters):
            s, self.data_frame = v(p_data_frame=self.data_frame).doFilte
        return True, self.data_frame
