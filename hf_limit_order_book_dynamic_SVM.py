import zipfile
import re
import csv
from datetime import datetime
from md_provider import *
from model.extract import *
from model.parameter import *
from model.training import *
from model.trade import *
from util.af_util import *

def naive_test():
    algo = Parameter()
    algo.metric = Metrics.PriceTrend
    sec_code = '600030.SH'    
    trade_date_list = get_trade_date_list('20151201', '20151231')
    for trade_date in trade_date_list:
        data = get_sec_md_dataset(trade_date, sec_code)
        fe = FeatureExtractor(sec_code, data, algo)
        m = fe.cal_feature()
        features = []
        features.extend(basic_features)
        features.extend(time_sensitive_features)
        features.extend(time_insensitive_features)
        logger.info("TradeDate={0}".format(trade_date))
        train_multi_class_svm(m, features)

def mock_trade_test():
    sec_code = '600030.SH'
    algo = Parameter()
    algo.metric = Metrics.PriceTrend   
    trade_date = '20151211'
    data = get_sec_md_dataset(trade_date, sec_code)
    fe = FeatureExtractor(sec_code, data, algo)
    m = fe.cal_feature()
    features = []
    features.extend(basic_features)
    features.extend(time_sensitive_features)
    features.extend(time_insensitive_features)
    trade_mocker = TradeMocker(sec_code, trade_date, algo, fe, features)


if __name__ == '__main__':
    begin_dt = datetime.now()
    naive_test()
    #mock_trade_test()
    
    end_dt = datetime.now()
    print("Total {0:0.2f} Seconds Used".format((end_dt - begin_dt).total_seconds()))
