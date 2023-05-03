#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
import pandas as pd


class CharlesFilterChain(object):
    """
    查尔斯，62岁，现任香港某教育集团董事长，有着传奇的人生经历。20年前，他以港股投资开始了自己的财富人生。
    查尔斯很少出现在媒体上，有人称他为投资圈的“隐士”，一起来认识这位低调的投资者。
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
