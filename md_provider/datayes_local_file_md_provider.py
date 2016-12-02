# -*- coding: utf-8 -*- 

import os
import zipfile
import csv
from collections import OrderedDict
from datetime import datetime
from md_provider.md_provider import *
from md_provider.md_data_type import *
from util.global_data import *

class DatayesLocalFileMDProvider(MDProvider):
    """
    201512-201603 数据，上海数据比较完整，深圳大量字段为空，不可使用
    """
    file_dir = "X:\\"

    @classmethod
    def get_data(cls, trade_date, sec_codes):
        result = {}
        target_file = "{0}\\{1}.zip".format(cls.file_dir, trade_date)
        if not os.path.exists(target_file):
            print("MarketData@{0} not exists".format(trade_date))
        pattern_code_dict = dict((cls.get_pattern_key(sec_code), sec_code) for sec_code in sec_codes)
        z = zipfile.ZipFile(target_file, "r")
        for filename in z.namelist():
            nodes = filename.split('/')
            if(len(nodes) < 2
               or not nodes[-1].endswith('csv')
               or not nodes[-2] in pattern_code_dict):
                continue
            sec_code = pattern_code_dict[nodes[-2]]
            if sec_code not in result:
                result[sec_code] = {}
            #MarketData
            if nodes[-1].startswith(MARKET_DATA_LABEL):
                md_dataset = cls.extract_market_data(z, filename)
                result[sec_code][MARKET_DATA_LABEL] = md_dataset
            #OrderQueue
            if nodes[-1].startswith(ORDER_QUEUE_LABEL):
                oq_dataset = cls.extract_order_queue(z, filename)
                result[sec_code][ORDER_QUEUE_LABEL] = oq_dataset
            #Transaction
            if nodes[-1].startswith(TRANSACTION_LABEL):
                tran_dataset = cls.extract_transaction(z, filename)
                result[sec_code][TRANSACTION_LABEL] = tran_dataset        
        z.close()
        return result

    @classmethod
    def get_pattern_key(cls, sec_code):
        split_codes = sec_code.split('.')
        pattern_code = sec_code
        if len(split_codes) >= 2:
            pattern_code = "{0}{1}".format(split_codes[1].upper(), split_codes[0])
        return pattern_code

    @classmethod
    def extract_market_data(cls, zip_file, csv_filename):
        result = OrderedDict()
        content = zip_file.read(csv_filename).decode('utf-8') .split("\n")
        spamreader = csv.reader(content, delimiter=',')
        row_count = 0
        for row in spamreader:
            row_count += 1
            if len(row) < 20:
                continue
            md = MarketDataEntry()
            try:
                md.timestamp = datetime.strptime(row[2] + row[3].ljust(9,'0'), '%Y%m%d%H%M%S%f')
                md.sec_code = row[1]
                md.last_price = float(row[8])
                md.acc_deal_volume = float(row[11])
                md.acc_deal_amount = float(row[12])
                md.open_price = float(row[5])
                md.min_price = float(row[7])
                md.max_price = float(row[6])
                md.close_price = float(row[9])
                md.pre_close_price = float(row[4])
                md.ask_prices.append(0 if row[13]=='' else float(row[13]))
                md.ask_volumes.append(0 if row[14]=='' else float(row[14]))
                md.ask_prices.append(0 if row[15]=='' else float(row[15]))
                md.ask_volumes.append(0 if row[16]=='' else float(row[16]))
                md.ask_prices.append(0 if row[17]=='' else float(row[17]))
                md.ask_volumes.append(0 if row[18]=='' else float(row[18]))
                md.ask_prices.append(0 if row[19]=='' else float(row[19]))
                md.ask_volumes.append(0 if row[20]=='' else float(row[20]))
                md.ask_prices.append(0 if row[21]=='' else float(row[21]))
                md.ask_volumes.append(0 if row[22]=='' else float(row[22]))
                md.ask_prices.append(0 if row[23]=='' else float(row[23]))
                md.ask_volumes.append(0 if row[24]=='' else float(row[24]))
                md.ask_prices.append(0 if row[25]=='' else float(row[25]))
                md.ask_volumes.append(0 if row[26]=='' else float(row[26]))
                md.ask_prices.append(0 if row[27]=='' else float(row[27]))
                md.ask_volumes.append(0 if row[28]=='' else float(row[28]))
                md.ask_prices.append(0 if row[29]=='' else float(row[29]))
                md.ask_volumes.append(0 if row[30]=='' else float(row[30]))
                md.ask_prices.append(0 if row[31]=='' else float(row[31]))
                md.ask_volumes.append(0 if row[32]=='' else float(row[32]))
                md.bid_prices.append(0 if row[33]=='' else float(row[33]))
                md.bid_volumes.append(0 if row[34]=='' else float(row[34]))
                md.bid_prices.append(0 if row[35]=='' else float(row[35]))
                md.bid_volumes.append(0 if row[36]=='' else float(row[36]))
                md.bid_prices.append(0 if row[37]=='' else float(row[37]))
                md.bid_volumes.append(0 if row[38]=='' else float(row[38]))
                md.bid_prices.append(0 if row[39]=='' else float(row[39]))
                md.bid_volumes.append(0 if row[40]=='' else float(row[40]))
                md.bid_prices.append(0 if row[41]=='' else float(row[41]))
                md.bid_volumes.append(0 if row[42]=='' else float(row[42]))
                md.bid_prices.append(0 if row[43]=='' else float(row[43]))
                md.bid_volumes.append(0 if row[44]=='' else float(row[44]))
                md.bid_prices.append(0 if row[45]=='' else float(row[45]))
                md.bid_volumes.append(0 if row[46]=='' else float(row[46]))
                md.bid_prices.append(0 if row[47]=='' else float(row[47]))
                md.bid_volumes.append(0 if row[48]=='' else float(row[48]))
                md.bid_prices.append(0 if row[49]=='' else float(row[49]))
                md.bid_volumes.append(0 if row[50]=='' else float(row[50]))
                md.bid_prices.append(0 if row[51]=='' else float(row[51]))
                md.bid_volumes.append(0 if row[52]=='' else float(row[52]))
                result[md.timestamp] = md
            except:
                pass
        return result

    @classmethod
    def extract_order_queue(cls, zip_file, csv_filename):
        result = OrderedDict()
        content = zip_file.read(csv_filename).decode('utf-8') .split("\n")
        spamreader = csv.reader(content, delimiter=',')
        row_count = 0
        for row in spamreader:
            row_count += 1
            if len(row) < 10:
                continue
            oq = OrderQueueEntry()
            try:
                oq.sec_code = row[1]
                oq.timestamp = datetime.strptime(row[2] + row[3].ljust(9,'0'), '%Y%m%d%H%M%S%f')
                oq.direction = row[4].upper()
                oq.price = float(row[5]) if len(row[5]) > 0 else 0.0
                oq.total_volume = float(row[6]) if len(row[6]) > 0 else 0
                oq.total_count = float(row[7]) if len(row[7]) > 0 else 0
                oq.ava_count = int(float(row[8]) if len(row[8]) > 0 else 0)
                oq.order_sizes = [float(size) if len(size)>0 else 0 for size in row[9:9 + oq.ava_count]]
                if oq.timestamp not in result:
                    result[oq.timestamp] = {}
                if oq.direction not in result[oq.timestamp]:
                    result[oq.timestamp][oq.direction] = []
                result[oq.timestamp][oq.direction].append(oq)
            except:
                pass
        return result

    @classmethod
    def extract_transaction(cls, zip_file, csv_filename):
        result = OrderedDict()
        content = zip_file.read(csv_filename).decode('utf-8') .split("\n")
        spamreader = csv.reader(content, delimiter=',')
        row_count = 0
        for row in spamreader:
            row_count += 1
            if len(row) < 10:
                continue
            tran = TransactionEntry()
            try:
                tran.sec_code = row[1]
                tran.timestamp = datetime.strptime(row[2] + row[3].ljust(9,'0'), '%Y%m%d%H%M%S%f')
                tran.price = float(row[4]) if len(row[4]) > 0 else 0.0
                tran.volume = float(row[5]) if len(row[5]) > 0 else 0.0 
                tran.order_id = float(row[7]) if len(row[7]) > 0 else 0.0 
                tran.direction = row[8]
                result[tran.timestamp] = tran
            except:
                pass
        return result
