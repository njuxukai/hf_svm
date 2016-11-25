# -*- coding: utf-8 -*- 
import math
import numpy as np
import pandas as pd
from sklearn.svm import SVC, LinearSVC
from sklearn import preprocessing
from datetime import datetime
from util.af_util import *
 
class TradeMocker(object):
    """
    """
    def __init__(self, sec_code, trade_date, parameter, feature_df, feature_list):
        self.sec_code = sec_code
        self.trade_date = trade_date
        self.parameter = parameter
        self.feature_df = feature_df
        self.feature_list = feature_list

    def simulate(self):
        """
            每次买/卖一股
            1 超时 平仓
            2 止损 平仓
            3 止盈？ 平仓
        """
        current_trade_count = 0
        current_position_volume = 0
        current_position_cost = 0
        current_position_timestamp = 0
        acc_profit = 0
        open_price = self.feature_df.iloc[0]['open_price']
        for i in range(self.parameter.min_sample_set_size, \
            len(self.feature_df)):
            current_timestamp = self.feature_df.iloc[i]['timestamp']
            #考虑平仓
            if current_trade_count >= self.parameter.max_trade_times and \
                current_position_volume == 0:
                break
            if current_position_volume != 0:
                #超时
                #止损
                profit = current_position_volume * (self.feature_df.iloc[i]["last_price"] - current_position_cost)
                if cal_trade_time_seconds(current_position_timestamp, current_timestamp) \
                >= self.parameter.predict_duration or profit < -1 * math.abs(self.parameter.cut_loss_rate):
                    profit = profit - 0.0015 * self.feature_df.iloc[i]['last_price']
                    acc_profit += profit
                    current_position_volume = 0
            else:
                if cal_close_market_seconds(current_timestamp) > 15 * 60:
                    continue
                if current_position_volume != 0:
                    continue
                sample_size = self.parameter.min_sample_set_size                
                current_ava_feature_df = self.feature_df.iloc[0:i].copy()
                current_ava_feature_df.dropna()
                if len(current_ava_feature_df) < sample_size + 1:
                    continue
                #moving window
                model_feature_df = current_ava_feature_df.iloc[-sample_size:]                    
                model, scaler = self.train_svm_model(model_feature_df)
                test_feature = np.array(self.feature_df.iloc[i])
                test_feature_minmax = scaler.transform(test_feature)
                test_class_label = model.predict(test_feature_minmax)
                if test_class_label[0] != 0:
                    current_position_volume = test_class_label[0] 
                    current_position_cost = self.feature_df.iloc[i]["last_price"]
                    current_trade_count += 1
        print("TradeTimes={0};TotalProfit={1};ProfitRatio={2:2p}".format(current_trade_count,\
            acc_profit/(open_price * current_trade_count)))
                
                    



    def train_svm_model(self, sample_df):
        svm_model = LinearSVC(C=2.0)
        feature_vector_narray = np.array(sample_df[self.feature_list])
        label_narray = np.array(sample_df.label)
        min_max_scaler = preprocessing.MinMaxScaler()
        feature_vector_narray_minmax = min_max_scaler.fit_transform(feature_vector_narray)
        svm_model.fit(feature_vector_narray_minmax, label_narray)
        return svm_model, min_max_scaler

        
            


        

         
