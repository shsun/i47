#!/usr/bin/python
# coding:utf-8
import math
from futu import *
from pandasql import sqldf
from app.charles import CharlesFilterChain


def main():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    success, df_hk = get_all_stocks_by_type(quote_ctx=quote_ctx, stock_type=Market.SH)
    codes = df_hk['code'].values.tolist()

    inline_frames = list()
    for i in range(0, math.ceil(len(codes) / 400)):
        sub_codes = codes[i * 400:(i + 1) * 400]
        # 每 30 秒内最多请求 60 次快照。每次请求，接口参数 股票代码列表 支持传入的标的数量上限是 400 个。
        ret, df = quote_ctx.get_market_snapshot(sub_codes)
        success, df = CharlesFilterChain(p_data_frame=df).doFilte()
        inline_frames.append(df)
        time.sleep(1)

    final_df = pd.concat(inline_frames)
    final_df = final_df[['code', 'pe_ttm_ratio', 'pb_ratio', 'total_market_val']]




    for index, row in final_df.iterrows():
        code = row.get('code', None)
        o = df_hk[df_hk['code'] == code]
        name = o.get('name', None)
        # final_df['name'] = name
        # sql = f'select * from df_hk where code="{code}"'
        # tiny_df = sqldf(sql, globals())
        a = 1
        pass

    print(final_df)

    print(final_df.shape[0])

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
