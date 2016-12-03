# -*- coding: utf-8 -*- 

import os
import csv
from md_provider.md_provider import *
from md_provider.md_data_type import *
from util.global_data import *


def load_csv(fname):
    if not os.path.isfile(fname):
        return []
    reader = csv.reader(open(fname))
    lines = [line for line in reader]
    result = []
    line_count = len(lines)
    for i in range(1, line_count):
        row = {}
        header_count = len(lines[0])
        row_count = len(lines[i])
        count = min(header_count, row_count)
        for j in range(count):
            row[lines[0][j]] = lines[i][j]
        result.append(row)
    return result
            
def convert_dict_to_market_data(row_dict):
    md = MarketDataEntry()
    factor = 10000
    if "TradingDay" in row_dict and "Time" in row_dict:
        md.timestamp = datetime.strptime(row_dict["ActionDay"] + row_dict["Time"].ljust(9, '0'), '%Y%m%d%H%M%S%f')
    if "WindCode" in row_dict:
        md.sec_code = row_dict['WindCode']
    if "High" in row_dict:
        md.max_price = float(row_dict["High"]) / factor
    if "Low" in row_dict:
        md.min_price = float(row_dict["Low"]) / factor
    if "Match" in row_dict:
        md.last_price = float(row_dict["Match"]) / factor
    if "Open" in row_dict:
        md.open_price = float(row_dict["Open"]) / factor
    if "PreClose" in row_dict:
        md.pre_close_price = float(row_dict["PreClose"]) / factor
    if "Turnover" in row_dict:
        md.acc_deal_amount = float(row_dict["Turnover"]) 
    if "Volume" in row_dict:
        md.acc_deal_volume = float(row_dict["Volume"])
    if "TotalAskVol" in row_dict:
        md.total_ask_vol = int(row_dict["TotalAskVol"])
    if "TotalBidVol" in row_dict:
        md.total_bid_vol = int(row_dict["TotalBidVol"])
    if "NumTrades" in row_dict:
        md.num_trades = int(row_dict["NumTrades"])
    if "WeightedAvgAskPrice" in row_dict:
        md.weighted_avg_ask_price = float(row_dict["WeightedAvgAskPrice"]) / factor
    if "WeightedAvgBidPrice" in row_dict:
        md.weighted_avg_bid_price = float(row_dict["WeightedAvgBidPrice"]) / factor
    for i in range(1,11):
        ask_price_label = "AskPrice{0}".format(i)
        bid_price_label = "BidPrice{0}".format(i)
        ask_volume_label = "AskVolume{0}".format(i)
        bid_volume_label = "BidVolume{0}".format(i)
        if ask_price_label in row_dict:
            md.ask_prices.append(float(row_dict[ask_price_label]) / factor)
        else:
            md.ask_prices.append(0.0)
        if bid_price_label in row_dict:
            md.bid_prices.append(float(row_dict[bid_price_label]) / factor)
        else:
            md.bid_prices.append(0.0)
        if ask_volume_label in row_dict:
            md.ask_volumes.append(float(row_dict[ask_volume_label]) / factor)
        else:
            md.ask_volumes.append(0.0)
        if bid_volume_label in row_dict:
            md.bid_volumes.append(float(row_dict[bid_volume_label]) / factor)
        else:
            md.bid_volumes.append(0.0)
    return md

def convert_dict_to_order_queue(row_dict):
    factor = 10000
    order_queue = OrderQueueEntry()
    if "ActionDay" in row_dict and "Time" in row_dict:
        order_queue.timestamp = datetime.strptime(row_dict["ActionDay"] + row_dict["Time"].ljust(9, '0'), '%Y%m%d%H%M%S%f')
    if "WindCode" in row_dict:
        order_queue.sec_code = row_dict['WindCode']
    if "Side" in row_dict:
        order_queue.direction = row_dict["Side"]
    if "price" in row_dict:
        order_queue.price = float(row_dict["Price"]) / factor
    if "ABItems" in row_dict:
        order_queue.total_count = int(row_dict["ABItems"])
    if "ABVolumes" in row_dict:
        order_queue.order_sizes = [int(i) for i in row_dict["ABVolumes"].split(":")]
    return order_queue

def convert_dict_to_transaction(row_dict):
    pass

def convert_dict_to_order(row_dict):
    pass

def convert_dict_to_index_data(row_dict):
    pass
 

class WindTDFCsvMDProvider(MDProvider):
    """
    20161201 ??ʼ????
    """
    file_dir = r"Z:\wind_tdf_level2"
    @classmethod
    def get_data(cls, trade_date, sec_codes):
        result = {}
        for sec_code in set(sec_codes):
            result[sec_code] = cls.get_single_stock_data(trade_date, sec_code)
        return result

    @classmethod
    def get_single_stock_data(cls, trade_date, sec_code):
        result = {}
        target_path = r"{0}/{1}/stock/{2}/".format(file_dir, trade_date,sec_code)
        if not os.path.exists(target_path):
            return None

        market_data_fname = target_path + 'MarketData.csv'
        rows = load_csv(market_data_fname)
        mds = [convert_dict_to_market_data(row) for row in rows]
        if len(mds) > 0:
            result[MARKET_DATA_LABEL] = mds

        order_queue_fname = target_path + 'OrderQueue.csv'
        rows = load_csv(order_queue_fname)
        order_queues = [convert_dict_to_order_queue(row) for row in rows]
        if len(order_queues) > 0:
            result[OREDER_QUEUE_LABEL] = order_queues
            
        transaction_fname = target_path + 'Transaction.csv'
        rows = load_csv(transaction_fname)
        transactions = [convert_dict_to_transaction(row) for row in rows]
        if len(transactions) > 0:
            result[TRANSACTION_LABEL] = transactions
        
        order_fname = target_path + 'Order.csv'
        rows = load_csv(order_fname)
        orders = [convert_dict_to_order(row) for row in rows]
        if len(orders) > 0:
            result[ORDER_LABEL] = orders

        index_code = get_index_code(sec_code)
        target_index_path =  r"{0}/{1}/index/{2}/".format(file_dir, trade_date,index_code)
        index_data_fname = target_index_path + 'IndexData.csv'
        rows =load_csv(index_data_fname)
        index_datas = [convert_dict_to_index_data(row) for row in rows]
        if len(index_datas) > 0:
            result[INDEX_DATA_LABEL] = index_datas

        return result


    


        