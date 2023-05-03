#!/usr/bin/python
# coding:utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet, math
from futu import *
import pandas as pd
from pandasql import sqldf, load_meat, load_births
from app.PBFilter import PBFilter
from app.PEFilter import PEFilter
from app.DYRFilter import TTMDYRFilter
from app.market_cap import CapFilter

def main():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    success, df_hk = get_all_stocks_by_type(quote_ctx=quote_ctx, stock_type=Market.HK)
    # success, df_sh = get_all_stocks_by_type(quote_ctx=quote_ctx, stock_type=Market.SH)

    codes = df_hk['code'].values.tolist()
    for i in range(0, math.ceil(len(codes) / 400)):
        sub_codes = codes[i * 400:(i + 1) * 400]
        print(i, len(sub_codes))
        # 每 30 秒内最多请求 60 次快照。
        # 每次请求，接口参数 股票代码列表 支持传入的标的数量上限是 400 个。
        ret, df = quote_ctx.get_market_snapshot(sub_codes)
        success, df = PBFilter(p_data_frame=df).doFilte()
        print('PBFilter', df.shape[0])
        success, df = PEFilter(p_data_frame=df).doFilte()
        print('PEFilter', df.shape[0])
        success, df = TTMDYRFilter(p_data_frame=df).doFilte()
        print('TTMDYRFilter', df.shape[0])
        success, df = CapFilter(p_data_frame=df).doFilte()
        print('CapFilter', df.shape[0])


        time.sleep(1)

    quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽
    return 0


def get_all_stocks_by_type(quote_ctx, stock_type=Market.HK):
    """

    :param quote_ctx:
    :param stock_type:
    :return:
    """
    ret_code, df = quote_ctx.get_stock_basicinfo(market=stock_type, stock_type=SecurityType.STOCK, code_list=None)
    if ret_code == RET_OK:
        # print(df.shape[0], df.shape[1])
        # print(df.iloc[0][0])
        success = True
    else:
        print('error', file=sys.stderr)
        df = None
        success = False

    return success, df


if __name__ == '__main__':
    status = main()
    # sys.exit(status)
