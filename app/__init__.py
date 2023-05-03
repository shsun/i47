#!/usr/bin/python
# coding=utf-8
import datetime, time, os, sys, json, functools, random, sqlite3, greenlet

"""
获取市场快照

:param code_list: 股票列表
:return: (ret, data)

        ret == RET_OK 返回pd dataframe数据，data.DataFrame数据, 数据列格式如下

        ret != RET_OK 返回错误字符串

        =======================   =============   ==============================================================================
        参数                       类型                        说明
        =======================   =============   ==============================================================================
        code                       str            股票代码
        update_time                str            更新时间(yyyy-MM-dd HH:mm:ss)，（美股默认是美东时间，港股A股默认是北京时间）
        last_price                 float          最新价格
        open_price                 float          今日开盘价
        high_price                 float          最高价格
        low_price                  float          最低价格
        prev_close_price           float          昨收盘价格
        volume                     int            成交数量
        turnover                   float          成交金额
        turnover_rate              float          换手率
        suspension                 bool           是否停牌(True表示停牌)
        listing_date               str            上市日期 (yyyy-MM-dd)
        equity_valid               bool           是否正股（为true时以下正股相关字段才有合法数值）
        issued_shares              int            发行股本
        total_market_val           float          总市值
        net_asset                  int            资产净值
        net_profit                 int            净利润
        earning_per_share          float          每股盈利
        outstanding_shares         int            流通股本
        net_asset_per_share        float          每股净资产
        circular_market_val        float          流通市值
        ey_ratio                   float          收益率（该字段为比例字段，默认不展示%）
        pe_ratio                   float          市盈率（该字段为比例字段，默认不展示%）
        pb_ratio                   float          市净率（该字段为比例字段，默认不展示%）
        pe_ttm_ratio               float          市盈率TTM（该字段为比例字段，默认不展示%）
        dividend_ttm               float          股息TTM
        dividend_ratio_ttm         float          股息率TTM（该字段为百分比字段，默认不展示%）
        dividend_lfy               float          股息LFY，上一年度派息
        dividend_lfy_ratio         float          股息率LFY（该字段为百分比字段，默认不展示
        stock_owner                str            窝轮所属正股的代码或期权的标的股代码
        wrt_valid                  bool           是否是窝轮（为true时以下窝轮相关的字段才有合法数据）
        wrt_conversion_ratio       float          换股比率（该字段为比例字段，默认不展示%）
        wrt_type                   str            窝轮类型，参见WrtType
        wrt_strike_price           float          行使价格
        wrt_maturity_date          str            格式化窝轮到期时间
        wrt_end_trade              str            格式化窝轮最后交易时间
        wrt_code                   str            窝轮对应的正股（此字段已废除,修改为stock_owner）
        wrt_recovery_price         float          窝轮回收价
        wrt_street_vol             float          窝轮街货量
        wrt_issue_vol              float          窝轮发行量
        wrt_street_ratio           float          窝轮街货占比（该字段为比例字段，默认不展示%）
        wrt_delta                  float          窝轮对冲值
        wrt_implied_volatility     float          窝轮引伸波幅
        wrt_premium                float          窝轮溢价
        wrt_leverage               float          杠杆比率（倍）
        wrt_ipop                   float          价内/价外（该字段为百分比字段，默认不展示%）
        wrt_break_even_point       float          打和点
        wrt_conversion_price       float          换股价
        wrt_price_recovery_ratio   float          距收回价（该字段为百分比字段，默认不展示%）
        wrt_score                  float          综合评分
        wrt_upper_strike_price     float          上限价，仅界内证支持该字段
        wrt_lower_strike_price     float          下限价，仅界内证支持该字段
        wrt_inline_price_status    str            界内界外，仅界内证支持该字段，参见PriceType
        lot_size                   int            每手股数
        price_spread               float          当前摆盘价差亦即摆盘数据的买档或卖档的相邻档位的报价差
        ask_price                  float          卖价
        bid_price                  float          买价
        ask_vol                    float          卖量
        bid_vol                    float          买量
        enable_margin              bool           是否可融资，如果为true，后两个字段才有意义
        mortgage_ratio             float          股票抵押率（该字段为百分比字段，默认不展示%）
        long_margin_initial_ratio  float          融资初始保证金率（该字段为百分比字段，默认不展示%）
        enable_short_sell          bool           是否可卖空，如果为true，后三个字段才有意义
        short_sell_rate            float          卖空参考利率（该字段为百分比字段，默认不展示%）
        short_available_volume     int            剩余可卖空数量
        short_margin_initial_ratio float          卖空（融券）初始保证金率（该字段为百分比字段，默认不展示%
        amplitude                  float          振幅（该字段为百分比字段，默认不展示%）
        avg_price                  float          平均价
        bid_ask_ratio              float          委比（该字段为百分比字段，默认不展示%）
        volume_ratio               float          量比
        highest52weeks_price       float          52周最高价
        lowest52weeks_price        float          52周最低价
        highest_history_price      float          历史最高价
        lowest_history_price       float          历史最低价
        option_valid               bool           是否是期权（为true时以下期权相关的字段才有合法数值）
        option_type                str            期权类型，参见OptionType
        strike_time                str            行权日（美股默认是美东时间，港股A股默认是北京时间）
        option_strike_price        float          行权价
        option_contract_size       int            每份合约数
        option_open_interest       int            未平仓合约数
        option_implied_volatility  float          隐含波动率
        option_premium             float          溢价
        option_delta               float          希腊值 Delta
        option_gamma               float          希腊值 Gamma
        option_vega                float          希腊值 Vega
        option_theta               float          希腊值 Theta
        option_rho                 float          希腊值 Rho
        option_net_open_interest   int            净未平仓合约数
        option_expiry_date_distance    int        距离到期日天数
        option_contract_nominal_value  float      合约名义金额
        option_owner_lot_multiplier    float      相等正股手数，指数期权无该字段
        option_area_type           str            期权地区类型，见 OptionAreaType_
        option_contract_multiplier float          合约乘数，指数期权特有字段
        index_option_type          str            指数期权类型，见 IndexOptionType
        index_raise_count          int            指数类型上涨支数
        index_fall_count           int            指数类型下跌支数
        index_requal_count         int            指数类型平盘支数
        plate_raise_count          int            板块类型上涨支数
        plate_fall_count           int            板块类型下跌支数
        plate_equal_count          int            板块类型平盘支数
        after_volume               int            盘后成交量
        after_turnover             double         盘后成交额
        sec_status                 str            股票状态， 参见SecurityStatus
        future_valid               bool           是否期货
        future_last_settle_price   float          昨结
        future_position            float          持仓量
        future_position_change     float          日增仓
        future_main_contract       bool           是否主连合约
        future_last_trade_time     string         只有非主连期货合约才有该字段
        trust_valid                bool           是否基金
        trust_dividend_yield       float          股息率
        trust_aum                  float          资产规模
        trust_outstanding_units    int            总发行量
        trust_netAssetValue        float          单位净值
        trust_premium              float          溢价
        trust_assetClass           string         资产类别
        =======================   =============   ==============================================================================
"""

class Stock(object):
    """

    """

    def __init__(self, p_dict:dict=None):
        super().__init__()
        self.code = p_dict.get('code', None)
        # update_time
        # last_price                 float          最新价格
        # open_price                 float          今日开盘价
        # high_price                 float          最高价格
        # low_price                  float          最低价格
        # prev_close_price           float          昨收盘价格
        # volume                     int            成交数量
        # turnover                   float          成交金额
        # turnover_rate              float          换手率
        # suspension                 bool           是否停牌(True表示停牌)
        # listing_date               str            上市日期 (yyyy-MM-dd)
        # equity_valid               bool           是否正股（为true时以下正股相关字段才有合法数值）
        # issued_shares              int            发行股本
        # total_market_val           float          总市值
        # net_asset                  int            资产净值
        # net_profit                 int            净利润
        # earning_per_share          float          每股盈利
        # outstanding_shares         int            流通股本
        # net_asset_per_share        float          每股净资产
        # circular_market_val        float          流通市值
        # ey_ratio                   float          收益率（该字段为比例字段，默认不展示%）
        # pe_ratio                   float          市盈率（该字段为比例字段，默认不展示%）
        # pb_ratio                   float          市净率（该字段为比例字段，默认不展示%）
        # pe_ttm_ratio               float          市盈率TTM（该字段为比例字段，默认不展示%）
        # dividend_ttm               float          股息TTM
        # dividend_ratio_ttm         float          股息率TTM（该字段为百分比字段，默认不展示%）
        # dividend_lfy               float          股息LFY，上一年度派息
        # dividend_lfy_ratio         float          股息率LFY（该字段为百分比字段，默认不展示
        # stock_owner                str            窝轮所属正股的代码或期权的标的股代码
        # wrt_valid                  bool           是否是窝轮（为true时以下窝轮相关的字段才有合法数据）
        # wrt_conversion_ratio       float          换股比率（该字段为比例字段，默认不展示%）
        # wrt_type                   str            窝轮类型，参见WrtType
        # wrt_strike_price           float          行使价格
        # wrt_maturity_date          str            格式化窝轮到期时间
        # wrt_end_trade              str            格式化窝轮最后交易时间
        # wrt_code                   str            窝轮对应的正股（此字段已废除,修改为stock_owner）
        # wrt_recovery_price         float          窝轮回收价
        # wrt_street_vol             float          窝轮街货量
        # wrt_issue_vol              float          窝轮发行量
        # wrt_street_ratio           float          窝轮街货占比（该字段为比例字段，默认不展示%）
        # wrt_delta                  float          窝轮对冲值
        # wrt_implied_volatility     float          窝轮引伸波幅
        # wrt_premium                float          窝轮溢价
        # wrt_leverage               float          杠杆比率（倍）
        # wrt_ipop                   float          价内/价外（该字段为百分比字段，默认不展示%）
        # wrt_break_even_point       float          打和点
        # wrt_conversion_price       float          换股价
        # wrt_price_recovery_ratio   float          距收回价（该字段为百分比字段，默认不展示%）
        # wrt_score                  float          综合评分
        # wrt_upper_strike_price     float          上限价，仅界内证支持该字段
        # wrt_lower_strike_price     float          下限价，仅界内证支持该字段
        # wrt_inline_price_status    str            界内界外，仅界内证支持该字段，参见PriceType
        # lot_size                   int            每手股数
        # price_spread               float          当前摆盘价差亦即摆盘数据的买档或卖档的相邻档位的报价差
        # ask_price                  float          卖价
        # bid_price                  float          买价
        # ask_vol                    float          卖量
        # bid_vol                    float          买量
        # enable_margin              bool           是否可融资，如果为true，后两个字段才有意义
        # mortgage_ratio             float          股票抵押率（该字段为百分比字段，默认不展示%）
        # long_margin_initial_ratio  float          融资初始保证金率（该字段为百分比字段，默认不展示%）
        # enable_short_sell          bool           是否可卖空，如果为true，后三个字段才有意义
        # short_sell_rate            float          卖空参考利率（该字段为百分比字段，默认不展示%）
        # short_available_volume     int            剩余可卖空数量
        # short_margin_initial_ratio float          卖空（融券）初始保证金率（该字段为百分比字段，默认不展示%
        # amplitude                  float          振幅（该字段为百分比字段，默认不展示%）
        # avg_price                  float          平均价
        # bid_ask_ratio              float          委比（该字段为百分比字段，默认不展示%）
        # volume_ratio               float          量比
        # highest52weeks_price       float          52周最高价
        # lowest52weeks_price        float          52周最低价
        # highest_history_price      float          历史最高价
        # lowest_history_price       float          历史最低价
        # option_valid               bool           是否是期权（为true时以下期权相关的字段才有合法数值）
        # option_type                str            期权类型，参见OptionType
        # strike_time                str            行权日（美股默认是美东时间，港股A股默认是北京时间）
        # option_strike_price        float          行权价
        # option_contract_size       int            每份合约数
        # option_open_interest       int            未平仓合约数
        # option_implied_volatility  float          隐含波动率
        # option_premium             float          溢价
        # option_delta               float          希腊值 Delta
        # option_gamma               float          希腊值 Gamma
        # option_vega                float          希腊值 Vega
        # option_theta               float          希腊值 Theta
        # option_rho                 float          希腊值 Rho
        # option_net_open_interest   int            净未平仓合约数
        # option_expiry_date_distance    int        距离到期日天数
        # option_contract_nominal_value  float      合约名义金额
        # option_owner_lot_multiplier    float      相等正股手数，指数期权无该字段
        # option_area_type           str            期权地区类型，见 OptionAreaType_
        # option_contract_multiplier float          合约乘数，指数期权特有字段
        # index_option_type          str            指数期权类型，见 IndexOptionType
        # index_raise_count          int            指数类型上涨支数
        # index_fall_count           int            指数类型下跌支数
        # index_requal_count         int            指数类型平盘支数
        # plate_raise_count          int            板块类型上涨支数
        # plate_fall_count           int            板块类型下跌支数
        # plate_equal_count          int            板块类型平盘支数
        # after_volume               int            盘后成交量
        # after_turnover             double         盘后成交额
        # sec_status                 str            股票状态， 参见SecurityStatus
        # future_valid               bool           是否期货
        # future_last_settle_price   float          昨结
        # future_position            float          持仓量
        # future_position_change     float          日增仓
        # future_main_contract       bool           是否主连合约
        # future_last_trade_time     string         只有非主连期货合约才有该字段
        # trust_valid                bool           是否基金
        # trust_dividend_yield       float          股息率
        # trust_aum                  float          资产规模
        # trust_outstanding_units    int            总发行量
        # trust_netAssetValue        float          单位净值
        # trust_premium              float          溢价
        # trust_assetClass           string         资产类别
