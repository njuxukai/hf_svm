# -*- coding: utf-8 -*- 
import pandas as pd
import numpy as np
import copy
from util import *

class FeatureExtractor(object):
    def __init__(self, sec_code, sec_data, parameter):
        self.sec_code = sec_code
        self.sec_data = sec_data
        self.parameter = parameter
        self.md_df = self.format_md_dataframe()
        self.feature_df = None

    def format_md_dataframe(self):
        """ 
        将md放入dataframe，内部函数
        """
        market_code = self.sec_code.split('.')[-1].upper()
        columns = ['open_price', 'last_price', 'ask_price1', 'ask_volume1', \
            'ask_price2', 'ask_volume2', 'ask_price3', 'ask_volume3', \
            'ask_price4', 'ask_volume4', 'ask_price5', 'ask_volume5', \
            'ask_price6', 'ask_volume6', 'ask_price7', 'ask_volume7', \
            'ask_price8', 'ask_volume8', 'ask_price9', 'ask_volume9', \
            'ask_price10', 'ask_volume10', \
            'bid_price1', 'bid_volume1', 'bid_price2', 'bid_volume2', \
            'bid_price3', 'bid_volume3', 'bid_price4', 'bid_volume4', \
            'bid_price5', 'bid_volume5', 'bid_price6', 'bid_volume6', \
            'bid_price7', 'bid_volume7', 'bid_price8', 'bid_volume8', \
            'bid_price9', 'bid_volume9', 'bid_price10', 'bid_volume10', \
            'acc_deal_volume', 'acc_deal_amount', 'pre_close_price']
        in_count = 0
        out_count = 0

        #iterator
        m = []
        index = []
        for (k, v) in self.sec_data[MARKET_DATA_LABEL].items():
            if not in_countinuous_auction(market_code, k):
                continue
            row = [v.open_price, v.last_price, v.ask_prices[0], v.ask_volumes[0], \
                v.ask_prices[1], v.ask_volumes[1], v.ask_prices[2], v.ask_volumes[2], \
                v.ask_prices[3], v.ask_volumes[3], v.ask_prices[4], v.ask_volumes[4], \
                v.ask_prices[5], v.ask_volumes[5], v.ask_prices[6], v.ask_volumes[6], \
                v.ask_prices[7], v.ask_volumes[7], v.ask_prices[8], v.ask_volumes[8], \
                v.ask_prices[9], v.ask_volumes[9], \
                v.bid_prices[0], v.bid_volumes[0], v.bid_prices[1], v.bid_volumes[1], \
                v.bid_prices[2], v.bid_volumes[2], v.bid_prices[3], v.bid_volumes[3], \
                v.bid_prices[4], v.bid_volumes[4], v.bid_prices[5], v.bid_volumes[5], \
                v.bid_prices[6], v.bid_volumes[6], v.bid_prices[7], v.bid_volumes[7], \
                v.bid_prices[8], v.bid_volumes[8], v.bid_prices[9], v.bid_volumes[9], \
                v.acc_deal_volume, v.acc_deal_amount, v.pre_close_price]
            m.append(row)
            index.append(k)        
        m = pd.DataFrame(m, columns=columns, index=index)
        return m

    def cal_feature(self):
        '''
            在特征dataframe上计算各类特征变量，无法计算的用nan
        '''
        #self.feature_df = pd.DataFrame(index=self.md_df.index)
        self.feature_df = copy.deepcopy(self.md_df)
        a, b = self.format_acc_tran_series()
        self.feature_df['acc_ask_deal_volume'] = a
        self.feature_df['acc_bid_deal_volume'] = b
        self.cal_basic_features()
        self.cal_time_insensitive_features()
        self.cal_time_sensitive_features()
        self.mark_label()
        self.cut_unecessary_data()
        return self.feature_df


    def cal_basic_features(self):
        self.feature_df['v1_ap1'] = self.feature_df['ask_price1']
        self.feature_df['v1_ap2'] = self.feature_df['ask_price2']
        self.feature_df['v1_ap3'] = self.feature_df['ask_price3']
        self.feature_df['v1_ap4'] = self.feature_df['ask_price4']
        self.feature_df['v1_ap5'] = self.feature_df['ask_price5']
        self.feature_df['v1_ap6'] = self.feature_df['ask_price6']
        self.feature_df['v1_ap7'] = self.feature_df['ask_price7']
        self.feature_df['v1_ap8'] = self.feature_df['ask_price8']
        self.feature_df['v1_ap9'] = self.feature_df['ask_price9']
        self.feature_df['v1_ap10'] = self.feature_df['ask_price10']
        self.feature_df['v1_av1'] = self.feature_df['ask_volume1']
        self.feature_df['v1_av2'] = self.feature_df['ask_volume2']
        self.feature_df['v1_av3'] = self.feature_df['ask_volume3']
        self.feature_df['v1_av4'] = self.feature_df['ask_volume4']
        self.feature_df['v1_av5'] = self.feature_df['ask_volume5']
        self.feature_df['v1_av6'] = self.feature_df['ask_volume6']
        self.feature_df['v1_av7'] = self.feature_df['ask_volume7']
        self.feature_df['v1_av8'] = self.feature_df['ask_volume8']
        self.feature_df['v1_av9'] = self.feature_df['ask_volume9']
        self.feature_df['v1_av10'] = self.feature_df['ask_volume10']
        self.feature_df['v1_bp1'] = self.feature_df['bid_price1']
        self.feature_df['v1_bp2'] = self.feature_df['bid_price2']
        self.feature_df['v1_bp3'] = self.feature_df['bid_price3']
        self.feature_df['v1_bp4'] = self.feature_df['bid_price4']
        self.feature_df['v1_bp5'] = self.feature_df['bid_price5']
        self.feature_df['v1_bp6'] = self.feature_df['bid_price6']
        self.feature_df['v1_bp7'] = self.feature_df['bid_price7']
        self.feature_df['v1_bp8'] = self.feature_df['bid_price8']
        self.feature_df['v1_bp9'] = self.feature_df['bid_price9']
        self.feature_df['v1_bp10'] = self.feature_df['bid_price10']
        self.feature_df['v1_bv1'] = self.feature_df['bid_volume1']
        self.feature_df['v1_bv2'] = self.feature_df['bid_volume2']
        self.feature_df['v1_bv3'] = self.feature_df['bid_volume3']
        self.feature_df['v1_bv4'] = self.feature_df['bid_volume4']
        self.feature_df['v1_bv5'] = self.feature_df['bid_volume5']
        self.feature_df['v1_bv6'] = self.feature_df['bid_volume6']
        self.feature_df['v1_bv7'] = self.feature_df['bid_volume7']
        self.feature_df['v1_bv8'] = self.feature_df['bid_volume8']
        self.feature_df['v1_bv9'] = self.feature_df['bid_volume9']
        self.feature_df['v1_bv10'] = self.feature_df['bid_volume10']

    def cal_time_insensitive_features(self):
        self.feature_df['v2_(a-b)1'] = self.feature_df['ask_price1'] - self.feature_df['bid_price1']
        self.feature_df['v2_(a-b)2'] = self.feature_df['ask_price2'] - self.feature_df['bid_price2']
        self.feature_df['v2_(a-b)3'] = self.feature_df['ask_price3'] - self.feature_df['bid_price3']
        self.feature_df['v2_(a-b)4'] = self.feature_df['ask_price4'] - self.feature_df['bid_price4']
        self.feature_df['v2_(a-b)5'] = self.feature_df['ask_price5'] - self.feature_df['bid_price5']
        self.feature_df['v2_(a-b)6'] = self.feature_df['ask_price6'] - self.feature_df['bid_price6']
        self.feature_df['v2_(a-b)7'] = self.feature_df['ask_price7'] - self.feature_df['bid_price7']
        self.feature_df['v2_(a-b)8'] = self.feature_df['ask_price8'] - self.feature_df['bid_price8']
        self.feature_df['v2_(a-b)9'] = self.feature_df['ask_price9'] - self.feature_df['bid_price9']
        self.feature_df['v2_(a-b)10'] = self.feature_df['ask_price10'] - self.feature_df['bid_price10']
        
        self.feature_df['v2_(a+b)1'] = (self.feature_df['ask_price1'] + self.feature_df['bid_price1']) / 2
        self.feature_df['v2_(a+b)2'] = (self.feature_df['ask_price2'] + self.feature_df['bid_price2']) / 2
        self.feature_df['v2_(a+b)3'] = (self.feature_df['ask_price3'] + self.feature_df['bid_price3']) / 2
        self.feature_df['v2_(a+b)4'] = (self.feature_df['ask_price4'] + self.feature_df['bid_price4']) / 2 
        self.feature_df['v2_(a+b)5'] = (self.feature_df['ask_price5'] + self.feature_df['bid_price5']) / 2
        self.feature_df['v2_(a+b)6'] = (self.feature_df['ask_price6'] + self.feature_df['bid_price6']) / 2
        self.feature_df['v2_(a+b)7'] = (self.feature_df['ask_price7'] + self.feature_df['bid_price7']) / 2
        self.feature_df['v2_(a+b)8'] = (self.feature_df['ask_price8'] + self.feature_df['bid_price8']) / 2
        self.feature_df['v2_(a+b)9'] = (self.feature_df['ask_price9'] + self.feature_df['bid_price9']) / 2
        self.feature_df['v2_(a+b)10'] = (self.feature_df['ask_price10'] + self.feature_df['bid_price10']) / 2

        self.feature_df['v3_a2-1'] = self.feature_df['ask_price2'] - self.feature_df['ask_price1']
        self.feature_df['v3_a3-1'] = self.feature_df['ask_price3'] - self.feature_df['ask_price1']
        self.feature_df['v3_a4-1'] = self.feature_df['ask_price4'] - self.feature_df['ask_price1']
        self.feature_df['v3_a5-1'] = self.feature_df['ask_price5'] - self.feature_df['ask_price1']
        self.feature_df['v3_a6-1'] = self.feature_df['ask_price6'] - self.feature_df['ask_price1']
        self.feature_df['v3_a7-1'] = self.feature_df['ask_price7'] - self.feature_df['ask_price1']
        self.feature_df['v3_a8-1'] = self.feature_df['ask_price8'] - self.feature_df['ask_price1']
        self.feature_df['v3_a9-1'] = self.feature_df['ask_price9'] - self.feature_df['ask_price1']
        self.feature_df['v3_a10-1'] = self.feature_df['ask_price10'] - self.feature_df['ask_price1']

        self.feature_df['v3_b1-2'] = self.feature_df['bid_price1'] - self.feature_df['bid_price2']
        self.feature_df['v3_b1-3'] = self.feature_df['bid_price1'] - self.feature_df['bid_price3']
        self.feature_df['v3_b1-4'] = self.feature_df['bid_price1'] - self.feature_df['bid_price4']
        self.feature_df['v3_b1-5'] = self.feature_df['bid_price1'] - self.feature_df['bid_price5']
        self.feature_df['v3_b1-6'] = self.feature_df['bid_price1'] - self.feature_df['bid_price6']
        self.feature_df['v3_b1-7'] = self.feature_df['bid_price1'] - self.feature_df['bid_price7']
        self.feature_df['v3_b1-8'] = self.feature_df['bid_price1'] - self.feature_df['bid_price8']
        self.feature_df['v3_b1-9'] = self.feature_df['bid_price1'] - self.feature_df['bid_price9']
        self.feature_df['v3_b1-10'] = self.feature_df['bid_price1'] - self.feature_df['bid_price10']

        self.feature_df['v3_a2-1'] = abs(self.feature_df['ask_price2'] - self.feature_df['ask_price1'])
        self.feature_df['v3_a3-2'] = abs(self.feature_df['ask_price3'] - self.feature_df['ask_price2'])
        self.feature_df['v3_a4-3'] = abs(self.feature_df['ask_price4'] - self.feature_df['ask_price3'])
        self.feature_df['v3_a5-4'] = abs(self.feature_df['ask_price5'] - self.feature_df['ask_price4'])
        self.feature_df['v3_a6-5'] = abs(self.feature_df['ask_price6'] - self.feature_df['ask_price5'])
        self.feature_df['v3_a7-6'] = abs(self.feature_df['ask_price7'] - self.feature_df['ask_price6'])
        self.feature_df['v3_a8-7'] = abs(self.feature_df['ask_price8'] - self.feature_df['ask_price7'])
        self.feature_df['v3_a9-8'] = abs(self.feature_df['ask_price9'] - self.feature_df['ask_price8'])
        self.feature_df['v3_a10-9'] = abs(self.feature_df['ask_price10'] - self.feature_df['ask_price9'])

        self.feature_df['v3_b2-1'] = abs(self.feature_df['bid_price2'] - self.feature_df['bid_price1'])
        self.feature_df['v3_b3-2'] = abs(self.feature_df['bid_price3'] - self.feature_df['bid_price2'])
        self.feature_df['v3_b4-3'] = abs(self.feature_df['bid_price4'] - self.feature_df['bid_price3'])
        self.feature_df['v3_b5-4'] = abs(self.feature_df['bid_price5'] - self.feature_df['bid_price4'])
        self.feature_df['v3_b6-5'] = abs(self.feature_df['bid_price6'] - self.feature_df['bid_price5'])
        self.feature_df['v3_b7-6'] = abs(self.feature_df['bid_price7'] - self.feature_df['bid_price6'])
        self.feature_df['v3_b8-7'] = abs(self.feature_df['bid_price8'] - self.feature_df['bid_price7'])
        self.feature_df['v3_b9-8'] = abs(self.feature_df['bid_price9'] - self.feature_df['bid_price8'])
        self.feature_df['v3_b10-9'] = abs(self.feature_df['bid_price10'] - self.feature_df['bid_price9'])

        ask_price_columns = ['ask_price1', 'ask_price2', 'ask_price3', 'ask_price4', 'ask_price5', \
            'ask_price6', 'ask_price7', 'ask_price8', 'ask_price9', 'ask_price10']
        ask_volume_columns = ['ask_volume1', 'ask_volume2', 'ask_volume3', 'ask_volume4', 'ask_volume5', \
            'ask_volume6', 'ask_volume7', 'ask_volume8', 'ask_volume9', 'ask_volume10' ]
        bid_price_columns = ['bid_price1', 'bid_price2', 'bid_price3', 'bid_price4', 'bid_price5', \
            'bid_price6', 'bid_price7', 'bid_price8', 'bid_price9', 'bid_price10']
        bid_volume_columns =['bid_volume1', 'bid_volume2', 'bid_volume3', 'bid_volume4', 'bid_volume5', \
            'bid_volume6', 'bid_volume7', 'bid_volume8', 'bid_volume9', 'bid_volume10']

        self.feature_df['v4_avg_ap'] = self.feature_df[ask_price_columns].sum(axis=1) / len(ask_price_columns)
        self.feature_df['v4_avg_av'] = self.feature_df[ask_volume_columns].sum(axis=1) / len(ask_volume_columns)

        self.feature_df['v4_avg_bp'] = self.feature_df[bid_price_columns].sum(axis=1) / len(bid_price_columns)
        self.feature_df['v4_avg_bv'] = self.feature_df[bid_volume_columns].sum(axis=1) / len(bid_volume_columns)

        self.feature_df['v5_sum(ap-bp)'] = self.feature_df[ask_price_columns].sum(axis=1) - self.feature_df[bid_price_columns].sum(axis=1)
        self.feature_df['v5_sum(av-bv)'] = self.feature_df[ask_volume_columns].sum(axis=1) - self.feature_df[bid_volume_columns].sum(axis=1)

    def cal_time_sensitive_features(self):
        """
            原文献中大部分特征无法获取
            
        """
        
       
        #v6, v7 delta_t = 3 
        self.feature_df['v6_dap1'] = self.feature_df['ask_price1'] - self.feature_df['ask_price1'].shift(1)
        self.feature_df['v6_dap2'] = self.feature_df['ask_price2'] - self.feature_df['ask_price2'].shift(1)
        self.feature_df['v6_dap3'] = self.feature_df['ask_price3'] - self.feature_df['ask_price3'].shift(1)
        self.feature_df['v6_dap4'] = self.feature_df['ask_price4'] - self.feature_df['ask_price4'].shift(1)
        self.feature_df['v6_dap5'] = self.feature_df['ask_price5'] - self.feature_df['ask_price5'].shift(1)
        self.feature_df['v6_dap6'] = self.feature_df['ask_price6'] - self.feature_df['ask_price6'].shift(1)
        self.feature_df['v6_dap7'] = self.feature_df['ask_price7'] - self.feature_df['ask_price7'].shift(1)
        self.feature_df['v6_dap8'] = self.feature_df['ask_price8'] - self.feature_df['ask_price8'].shift(1)
        self.feature_df['v6_dap9'] = self.feature_df['ask_price9'] - self.feature_df['ask_price9'].shift(1)
        self.feature_df['v6_dap10'] = self.feature_df['ask_price10'] - self.feature_df['ask_price10'].shift(1)

        self.feature_df['v6_dav1'] = self.feature_df['ask_volume1'] - self.feature_df['ask_volume1'].shift(1)
        self.feature_df['v6_dav2'] = self.feature_df['ask_volume2'] - self.feature_df['ask_volume2'].shift(1)
        self.feature_df['v6_dav3'] = self.feature_df['ask_volume3'] - self.feature_df['ask_volume3'].shift(1)
        self.feature_df['v6_dav4'] = self.feature_df['ask_volume4'] - self.feature_df['ask_volume4'].shift(1)
        self.feature_df['v6_dav5'] = self.feature_df['ask_volume5'] - self.feature_df['ask_volume5'].shift(1)
        self.feature_df['v6_dav6'] = self.feature_df['ask_volume6'] - self.feature_df['ask_volume6'].shift(1)
        self.feature_df['v6_dav7'] = self.feature_df['ask_volume7'] - self.feature_df['ask_volume7'].shift(1)
        self.feature_df['v6_dav8'] = self.feature_df['ask_volume8'] - self.feature_df['ask_volume8'].shift(1)
        self.feature_df['v6_dav9'] = self.feature_df['ask_volume9'] - self.feature_df['ask_volume9'].shift(1)
        self.feature_df['v6_dav10'] = self.feature_df['ask_volume10'] - self.feature_df['ask_volume10'].shift(1)

        self.feature_df['v6_dbp1'] = self.feature_df['bid_price1'] - self.feature_df['bid_price1'].shift(1)
        self.feature_df['v6_dbp2'] = self.feature_df['bid_price2'] - self.feature_df['bid_price2'].shift(1)
        self.feature_df['v6_dbp3'] = self.feature_df['bid_price3'] - self.feature_df['bid_price3'].shift(1)
        self.feature_df['v6_dbp4'] = self.feature_df['bid_price4'] - self.feature_df['bid_price4'].shift(1)
        self.feature_df['v6_dbp5'] = self.feature_df['bid_price5'] - self.feature_df['bid_price5'].shift(1)
        self.feature_df['v6_dbp6'] = self.feature_df['bid_price6'] - self.feature_df['bid_price6'].shift(1)
        self.feature_df['v6_dbp7'] = self.feature_df['bid_price7'] - self.feature_df['bid_price7'].shift(1)
        self.feature_df['v6_dbp8'] = self.feature_df['bid_price8'] - self.feature_df['bid_price8'].shift(1)
        self.feature_df['v6_dbp9'] = self.feature_df['bid_price9'] - self.feature_df['bid_price9'].shift(1)
        self.feature_df['v6_dbp10'] = self.feature_df['bid_price10'] - self.feature_df['bid_price10'].shift(1)

        self.feature_df['v6_dbv1'] = self.feature_df['bid_volume1'] - self.feature_df['bid_volume1'].shift(1)
        self.feature_df['v6_dbv2'] = self.feature_df['bid_volume2'] - self.feature_df['bid_volume2'].shift(1)
        self.feature_df['v6_dbv3'] = self.feature_df['bid_volume3'] - self.feature_df['bid_volume3'].shift(1)
        self.feature_df['v6_dbv4'] = self.feature_df['bid_volume4'] - self.feature_df['bid_volume4'].shift(1)
        self.feature_df['v6_dbv5'] = self.feature_df['bid_volume5'] - self.feature_df['bid_volume5'].shift(1)
        self.feature_df['v6_dbv6'] = self.feature_df['bid_volume6'] - self.feature_df['bid_volume6'].shift(1)
        self.feature_df['v6_dbv7'] = self.feature_df['bid_volume7'] - self.feature_df['bid_volume7'].shift(1)
        self.feature_df['v6_dbv8'] = self.feature_df['bid_volume8'] - self.feature_df['bid_volume8'].shift(1)
        self.feature_df['v6_dbv9'] = self.feature_df['bid_volume9'] - self.feature_df['bid_volume9'].shift(1)
        self.feature_df['v6_dbv10'] = self.feature_df['bid_volume10'] - self.feature_df['bid_volume10'].shift(1)
    
        self.feature_df['v7_avg_ask_rate'] = (self.feature_df['acc_ask_deal_volume'] - self.feature_df['acc_ask_deal_volume'].shift(1)) / 3
        self.feature_df['v7_avg_bid_rate'] = (self.feature_df['acc_bid_deal_volume'] - self.feature_df['acc_bid_deal_volume'].shift(1)) / 3
        
        T_interval = self.parameter.T / 3
        t_interval = self.parameter.t / 3
        self.feature_df['v8_ask_lambda'] = (self.feature_df['acc_ask_deal_volume'] - self.feature_df['acc_ask_deal_volume'].shift(t_interval)) / self.parameter.t -\
            (self.feature_df['acc_ask_deal_volume'] - self.feature_df['acc_ask_deal_volume'].shift(T_interval)) / self.parameter.T 
        self.feature_df['v8_ask_lambda'][self.feature_df['v8_ask_lambda'] > 0] = 1
        self.feature_df['v8_ask_lambda'][self.feature_df['v8_ask_lambda'] <= 0] = 0

        self.feature_df['v8_bid_lambda'] = (self.feature_df['acc_bid_deal_volume'] - self.feature_df['acc_bid_deal_volume'].shift(t_interval)) / self.parameter.t -\
            (self.feature_df['acc_bid_deal_volume'] - self.feature_df['acc_bid_deal_volume'].shift(T_interval)) / self.parameter.T 
        self.feature_df['v8_bid_lambda'][self.feature_df['v8_bid_lambda'] > 0] = 1
        self.feature_df['v8_bid_lambda'][self.feature_df['v8_bid_lambda'] <= 0] = 0

    def cal_extension_features(self):
        """
        新增特征：
        1 当前涨跌幅
        2 当前跟踪指数涨跌幅
        """ 
        self.feature_df["pct_chg"] = 100 * (self.feature_df["last_price"] / self.feature_df["pre_close_price"] - 1)
        self.feature_df["almost_high_limit"] = 1 * (self.feature_df["pct_chg"] >= 7)
        self.feature_df["almost_low_limit"] = 1 * (self.feature_df["pct_chg"] <= -7)
        
        
        pass


    def mark_label(self):
        '''
            在特征dataframe上对特征向量打标签，完成该步骤后，删除所有含有nan的行
        '''
        if self.parameter.metric == Metrics.MidPriceMovement:
            self.mark_mid_price_movement_label()
        if self.parameter.metric == Metrics.BidAskSpreadCrossingDirection:
            self.mark_ask_bid_spread_crossing_direction_label()
        if self.parameter.metric == Metrics.PriceTrend:
            self.mark_price_trend_label()

    def mark_mid_price_movement_label(self):
        """
        
        """
        predict_interval = self.parameter.predict_duration / 3
        mid_price_series = (self.feature_df['ask_price1'] + self.feature_df['bid_price1']) / 2
        mid_price_chg_series = mid_price_series.shift(-predict_interval) - mid_price_series

        threshold = 0.01
        def f(x):
            if x <= -threshold:
                return -1
            if x >= threshold:
                return 1
            if x < threshold and x>-threshold:
                return 0
            return x
        self.feature_df['label'] = mid_price_chg_series.map(f)

    def mark_ask_bid_spread_crossing_direction_label(self):
        pass

    def mark_price_trend_label(self):
        """
        """
        predict_interval = int(self.parameter.predict_duration / 3)
        last_price_series = self.feature_df['last_price'].shift(-predict_interval) - \
            self.feature_df['last_price']
        threshold = self.parameter.predict_trend_rate * self.feature_df['open_price'][0]
        last_price_series.dropna()
        self.feature_df['label'] = 1 * (last_price_series >= threshold) + \
            (-1) * (last_price_series <= -threshold)
        #for i in range(len(self.feature_df) - predict_interval):
        #    min_price = np.max(self.feature_df['last_price'][i:i+predict_interval]) 
        #    max_price = np.max(self.feature_df['last_price'][i:i+predict_interval])
           
                                  

    def cut_unecessary_data(self):
        #self.feature_df = self.feature_df.drop(self.md_df.columns, axis=1)
        self.feature_df = self.feature_df.dropna()

    def format_acc_tran_series(self):
        """
        根据md_df的index 生成累计交易序列（区分买卖,两个序列）
        方便计算md之间的交易量
        """
        timestamps = self.md_df.index
        cur_ts_index = 0
        acc_bid_deal_volume = 0
        acc_ask_deal_volume = 0
        acc_bid_deal_volume_series = pd.Series(index=timestamps)
        acc_ask_deal_volume_series = pd.Series(index=timestamps)
        try:
            for trans in  self.sec_data[TRANSACTION_LABEL].values():
                while cur_ts_index < len(timestamps) \
                    and trans.timestamp > timestamps[cur_ts_index]:
                    acc_bid_deal_volume_series[timestamps[cur_ts_index]] \
                    = acc_bid_deal_volume
                    acc_ask_deal_volume_series[timestamps[cur_ts_index]] \
                    = acc_ask_deal_volume
                    cur_ts_index += 1
                if trans.direction == TRANSACTION_BID_DIRECTION:
                    acc_bid_deal_volume += trans.volume
                else:
                    acc_ask_deal_volume += trans.volume
        except:
            pass
        if cur_ts_index < len(timestamps):
            for i in range(cur_ts_index, len(timestamps)):
                acc_bid_deal_volume_series[timestamps[i]] = acc_bid_deal_volume
                acc_ask_deal_volume_series[timestamps[i]] = acc_ask_deal_volume
        return acc_ask_deal_volume_series, acc_bid_deal_volume_series



    


