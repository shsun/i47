#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
import pandas as pd

from app.charles import PBFilter, PEFilter, TTMDYRFilter, CapFilter


class CharlesFilterChain(object):
    """
    查尔斯，62岁，现任香港某教育集团董事长，有着传奇的人生经历。20年前，他以港股投资开始了自己的财富人生。
    查尔斯很少出现在媒体上，有人称他为投资圈的“隐士”，一起来认识这位低调的投资者。
    """

    def __init__(self, p_data_frame: pd.DataFrame):
        super().__init__()
        self.data_frame = p_data_frame

    def doFilte(self) -> (bool, pd.DataFrame):
        df = self.data_frame
        success, df = PBFilter(p_data_frame=df).doFilte()
        # print('PBFilter', df.shape[0])
        success, df = PEFilter(p_data_frame=df).doFilte()
        # print('PEFilter', df.shape[0])
        success, df = TTMDYRFilter(p_data_frame=df).doFilte()
        # print('TTMDYRFilter', df.shape[0])
        success, df = CapFilter(p_data_frame=df).doFilte()
        return True, df
