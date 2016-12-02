# -*- coding: utf-8 -*- 

import os
import csv
from md_provider.md_provider import *
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
    pass

def convert_dict_to_order_queue(row_dict):
    pass

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


    


        