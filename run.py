#!/usr/bin/python
# coding:utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
from futu import *
import pandas as pd
from pandasql import sqldf, load_meat, load_births


def main():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    success, df_hk = get_all_stocks_by_type(quote_ctx=quote_ctx, stock_type=Market.HK)
    success, df_sh = get_all_stocks_by_type(quote_ctx=quote_ctx, stock_type=Market.SH)

    pysqldf = lambda q: sqldf(q, globals())

    # >> > meat = load_meat()
    # >> > births = load_births()
    print(pysqldf("SELECT * FROM meat LIMIT 10;").head())

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
        print(df.shape[0], df.shape[1])
        print(df.iloc[0][0])
        success = True
    else:
        print('error', file=sys.stderr)
        df = None
        success = False

    return success, df


if __name__ == '__main__':
    status = main()
    # sys.exit(status)
