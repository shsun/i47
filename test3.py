#!/usr/bin/python
# coding:utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet
from futu import *

os.environ['PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION'] = "python"
#PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python python -c "from google.protobuf.internal import api_implementation; print(api_implementation._default_implementation_type)"

quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

ret, data = quote_ctx.get_ipo_list(Market.HK)
if ret == RET_OK:
    print(data)
    print(data['code'][0])  # 取第一条的股票代码
    print(data['code'].values.tolist())  # 转为 list
else:
    print('error:', data)
quote_ctx.close()  # 结束后记得关闭当条连接，防止连接条数用尽
