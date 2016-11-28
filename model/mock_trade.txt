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
            Ã¿´ÎÂò/ÂôÒ»¹É
            1 ³¬Ê± Æ½²Ö
            2 Ö¹Ëð Æ½²Ö
            3 Ö¹Ó¯£¿ Æ½²Ö
        """
        current_trade_count = 0
        current_position_volume = 0
        current_position_cost = 0
        current_position_timestamp = 0
        acc_profit = 0
        for i in range(self.parameter.min_sample_set_size, \
            len(self.feature_df)):
            current_timestamp = self.feature_df.irow[i]['timestamp']
            #¿¼ÂÇÆ½²Ö
            if current_trade_count >= self.parameter.max_trade_times and \
                current_position_volume == 0:
                break
            if current_position_volume != 0:
                #³¬Ê±
                #Ö¹Ëð
                profit = current_position_volume * (self.feature_df.iloc[i]["last_price"] - current_position_cost)
                if cal_trade_time_seconds(current_position_timestamp, current_timestamp) \
                >= self.parameter.predict_duration or profit < -1 * math.abs(self.parameter.cut_loss_rate):
                    profit = profit - 0.0015 * self.feature_df.iloc[i]['last_price']
                    acc_profit += profit
                    current_position_volume = 0
            else:
                sample_size = self.parameter.min_sample_set_size
                if i < sample_size:
                    continue
                current_ava_feature_df = self.feature_df.iloc[0:i]
                current_ava_feature_df.dropna()
                #moving window
                model_feature_df = current_ava_feature_df.iloc[-sample_size:]
                
                

                    
                    
                train_feature_df = self.feature_df.iloc[i-self.parameter.min_sample_set_size:i]

    def train_svm_model(self, sample_df):
        svm_model = LinearSVC(C=2.0)
        feature_vector_narray = np.array(sample_df[self.feature_list])
        label_narray = np.array(sample_df.label)
        min_max_scaler = preprocessing.MinMaxScaler()

        svm_model.fit(feature_vector_narray, label_narray)

        
            


        

         
