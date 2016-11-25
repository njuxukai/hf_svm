import attr
from datetime import datetime

@attr.s
class MarketDataEntry(object):
    sec_code = attr.ib(default='')
    timestamp = attr.ib(default=datetime.now())
    last_price = attr.ib(default = 0.0)
    acc_deal_volume = attr.ib(default = 0.0)
    acc_deal_amount = attr.ib(default = 0.0)
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
    price = attr.ib(default=0.0)
    volume = attr.ib(default=0.0)
    order_id = attr.ib(default=0)
    direction = attr.ib(default='N') 