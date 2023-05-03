#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
import pandas as pd

"""
每年分红3-5%


dividend_ratio_ttm	        float	股息率 TTM  
dividend_lfy_ratio	        float	股息率 LFY
trust_dividend_yield	    float	股息率


股息率（Dividend Yield Ratio），是一年的总派息额与当时市价的比例。以占股票最后销售价格的百分数表示的年度股息，该指标是投资收益率的简化形式。
股息率是股息与股票价格之间的比率。
"""


class TTMDYRFilter(object):
    """

    """

    def __init__(self, p_data_frame: pd.DataFrame):
        super().__init__()
        self.data_frame = p_data_frame

    def doFilte(self) -> (bool, pd.DataFrame):
        success, df = None, None
        self.data_frame = self.data_frame[self.data_frame['dividend_ratio_ttm'] >= 3]
        return success, self.data_frame
