# -*- coding: utf-8 -*- 

import os
import csv
from md_provider.md_provider import *
from md_provider.md_data_type import *
from util.global_data import *
from util.af_util import get_index_code
from collections import OrderedDict


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
    factor = 10000
    transaction = TransactionEntry()
    if "ActionDay" in row_dict and "Time" in row_dict:
        transaction.timestamp = datetime.strptime(row_dict["ActionDay"] + row_dict["Time"].ljust(9, '0'), '%Y%m%d%H%M%S%f')
    if "WindCode" in row_dict:
        transaction.sec_code = row_dict['WindCode']
    if "BSFlag" in row_dict:
        transaction.direction = row_dict["BSFlag"]
    if "Price" in row_dict:
        transaction.price = float(row_dict["Price"]) / factor
    if "Volume" in row_dict:
        transaction.volume = int(row_dict["Volume"])
    if "AskOrder" in row_dict:
        transaction.ask_order_sno = int(row_dict["AskOrder"])
    if "BidOrder" in row_dict:
        transaction.bid_order_sno = int(row_dict["BidOrder"])
    if "FunctionCode" in row_dict:
        transaction.function_code = str(row_dict["FunctionCode"])
    if "Index" in row_dict:
        transaction.index = int(row_dict["Index"])
    if "OrderKind" in row_dict:
        transaction.order_kind = str(row_dict["OrderKind"]) 
    return transaction


def convert_dict_to_order(row_dict):
    factor = 10000
    order = OrderEntry()
    if "ActionDay" in row_dict and "Time" in row_dict:
        order.timestamp = datetime.strptime(row_dict["ActionDay"] + row_dict["Time"].ljust(9, '0'), '%Y%m%d%H%M%S%f')
    if "WindCode" in row_dict:
        order.sec_code = row_dict['WindCode']
    if "FunctionCode" in row_dict:
        order.function_code = str(row_dict["FunctionCode"])
    if "Order" in row_dict:
        order.order_sno = int(row_dict["Order"])
    if "OrderKind" in row_dict:
        order.order_kind = str(row_dict["OrderKind"])
    if "Price" in row_dict:
        order.order_price = float(row_dict["Price"]) / factor
    if "Volume" in row_dict:
        order.order_volume = int(row_dict["Volume"])
    return order


def convert_dict_to_index_data(row_dict):
    index_data = IndexDataEntry()
    factor = 10000
    if "ActionDay" in row_dict and "Time" in row_dict:
        index_data.timestamp = datetime.strptime(row_dict["ActionDay"] + row_dict["Time"].ljust(9, '0'), '%Y%m%d%H%M%S%f')
    if "WindCode" in row_dict:
        index_data.sec_code = row_dict['WindCode']
    if "HighIndex" in row_dict:
        index_data.high_index = float(row_dict["HighIndex"]) / factor
    if "LastIndex" in row_dict:
        index_data.last_index = float(row_dict["LastIndex"]) / factor
    if "LowIndex" in row_dict:
        index_data.low_index = float(row_dict["LowIndex"]) / factor
    if "OpenIndex" in row_dict:
        index_data.open_index = float(row_dict["OpenIndex"]) / factor
    if "PreCloseIndex" in row_dict:
        index_data.preclose_index = float(row_dict["PreCloseIndex"]) / factor 
    if "TotalVolume" in row_dict:
        index_data.acc_trade_volume = int(row_dict["TotalVolume"]) 
    if "Turnover" in row_dict:
        index_data.acc_trade_amount = int(row_dict["Turnover"])
    return index_data


class WindTDFCsvMDProvider(MDProvider):
    """
    20161201 TDF行情接口盘后
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

        market_data_dict = OrderedDict()
        market_data_fname = target_path + 'MarketData.csv'
        rows = load_csv(market_data_fname)
        for row in rows:
            md = convert_dict_to_market_data(row)
            market_data_dict[md.timestamp] = md
        result[MARKET_DATA_LABEL] = market_data_dict

        order_queue_dict = OrderedDict()
        order_queue_fname = target_path + 'OrderQueue.csv'
        rows = load_csv(order_queue_fname)
        for row in rows:
            queue = convert_dict_to_order_queue(row)
            if queue.timestamp not in order_queue_dict:
                order_queue_dict[queue.timestamp] = {}
            order_queue_dict[queue.timestamp][queue.direction] = queue
            result[OREDER_QUEUE_LABEL] = order_queue_dict
            
        transaction_dict = OrderedDict()
        transaction_fname = target_path + 'Transaction.csv'
        rows = load_csv(transaction_fname)
        for row in rows:
            transaction = convert_dict_to_transaction(row)
            transaction_dict[transaction.timestamp] = transaction
        result[TRANSACTION_LABEL] = transaction_dict
        
        order_dict = OrderedDict()
        order_fname = target_path + 'Order.csv'
        rows = load_csv(order_fname)
        for row in rows:
            order = convert_dict_to_order(row)
            order_dict[order.timestamp] = order
        result[ORDER_LABEL] = order_dict

        index_data_dict = OrderedDict()
        index_code = get_index_code(sec_code)
        target_index_path =  r"{0}/{1}/index/{2}/".format(file_dir, trade_date,index_code)
        index_data_fname = target_index_path + 'IndexData.csv'
        rows =load_csv(index_data_fname)
        for row in rows:
            index_data = convert_dict_to_index_data(row)
            index_data_dict[index_data.timestamp] = index_data
        result[INDEX_DATA_LABEL] = index_data_dict

        return result


    


        