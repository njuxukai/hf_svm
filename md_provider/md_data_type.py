﻿import attr
from datetime import datetime

@attr.s
class MarketDataEntry(object):
    sec_code = attr.ib(default='')
    timestamp = attr.ib(default=datetime.now())
    last_price = attr.ib(default = 0.0)
    acc_deal_volume = attr.ib(default = 0.0)
    acc_deal_amount = attr.ib(default = 0.0)
    total_ask_vol = attr.ib(default = 0)
    total_bid_vol = attr.ib(default = 0)
    weighted_avg_ask_price = attr.ib(default = 0.0)
    weighted_avg_bid_price = attr.ib(default =0.0)
    num_trades = attr.ib(default = 0)
    high_limit = attr.ib(default = 0.0)
    low_limit = attr.ib(default = 0.0)
    open_price = attr.ib(default = 0.0)
    min_price = attr.ib(default = 0.0)
    max_price = attr.ib(default = 0.0)
    close_price = attr.ib(default = 0.0)
    pre_close_price = attr.ib(default = 0.0)
    ask_prices = attr.ib(default=attr.Factory(list))
    bid_prices = attr.ib(default=attr.Factory(list))
    ask_volumes = attr.ib(default=attr.Factory(list))
    bid_volumes = attr.ib(default=attr.Factory(list))


@attr.s
class OrderQueueEntry(object):
    sec_code = attr.ib(default='')
    timestamp = attr.ib(default=datetime.now())
    direction = attr.ib(default='B')
    price = attr.ib(default=0.0)
    total_volume = attr.ib(default=0.0)
    total_count = attr.ib(default=0)
    ava_count = attr.ib(default=0)
    order_sizes = attr.ib(default=attr.Factory(list))


@attr.s
class TransactionEntry(object):
    sec_code = attr.ib(default='')
    timestamp = attr.ib(default=datetime.now())
    ask_order_sno = attr.ib(default=0)
    bid_order_sno = attr.ib(default=0)
    direction = attr.ib(default='B')
    function_code = attr.ib(default='0')
    index = attr.ib(default=0)
    order_kind = attr.ib(default='0')    
    price = attr.ib(default=0.0)
    volume = attr.ib(default=0.0)



@attr.s
class OrderEntry(object):
    sec_code = attr.ib(default='')
    timestamp = attr.ib(default=datetime.now())
    function_code = attr.ib(default='B')
    order_kind = attr.ib(default='0')
    order_sno = attr.ib(default=0)
    order_price = attr.ib(default=0)
    order_volume = attr.ib(default=0)
    

@attr.s
class IndexDataEntry(object):
    index_code = attr.ib(default='')
    timestamp = attr.ib(default=datetime.now())
    last_index = attr.ib(default=0)
    high_index = attr.ib(default=0)
    low_index = attr.ib(default=0)
    open_index = attr.ib(default=0)
    preclose_index = attr.ib(default=0)
    acc_trade_volume = attr.ib(default=0)
    acc_trade_amount = attr.ib(default=0)
    
