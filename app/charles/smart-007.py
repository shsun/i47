#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3
import pandas
import futu

"""
回测策略：找到过去m个交易日跌幅最大的股票，计算该股票未来n个交易日的涨幅。计算出该股票的盈利概率。
"""


class XYZ(object):
    """

    """

    def __init__(self, quote_ctx: futu.OpenQuoteContext = None, stock_basicinfo: dict = None, m: int = 1, n: int = 1):
        super().__init__()
        self.quote_ctx = quote_ctx
        self.stock_basicinfo = stock_basicinfo
        self.m = m
        self.n = n

    def execute(self) -> (bool, float):
        success, r = None, 0.1
        return success, r
