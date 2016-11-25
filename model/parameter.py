import attr
from util.global_data import *

@attr.s
class Parameter(object):
    metric = attr.ib(default=Metrics.MidPriceMovement)
    T = attr.ib(default = 1800)
    t = attr.ib(default = 600)
    predict_duration = attr.ib(default=600)
    min_sample_set_size = attr.ib(default=300)
    max_trade_times = attr.ib(default=10)
    cut_loss_rate = attr.ib(default = 0.002)
    