#!/usr/bin/python
# coding:utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
from futu import *


def main():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    ret, data = quote_ctx.get_ipo_list(Market.HK)
    if ret == RET_OK:
        print(data)
        print(data['code'][0])  # 取第一条的股票代码
        print(data['code'].values.tolist())  # 转为 list
        print(len(data))
    else:
        print('error:', data)
    quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽
    return 0


if __name__ == '__main__':
    status = main()
    # sys.exit(status)
