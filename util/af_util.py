+# -*- coding: utf-8 -*- 
import os
import pickle
from datetime import datetime
from md_provider import *
from util.global_data import *
import sqlite3
local_db_string = 'local.db'

def get_index_code(sec_code):
    """
    TODO
    """
    pass

def qry_local_db(sql):
    conn = sqlite3.connect(local_db_string)
    curs = conn.cursor()
    curs = curs.execute(sql)
    result = curs.fetchall()
    conn.commit()
    curs.close()
    conn.close()
    return result

def get_trade_date_list(begin_date, end_date):
    qry_sql = ( "select cur_date from t_trade_day "
                "where cur_date between '{0}' and '{1}' order by 1")
    data = qry_local_db(qry_sql.format(begin_date, end_date))
    result = []
    for row in data:
        result.append(row[0])
    return result

def get_sec_md_dataset(trade_date, sec_code):
    """
    该函数为调试生成，将通联的数据暂存在本地目录下
    """
    cache_filename = "{0}_{1}.pk".format(trade_date, sec_code)
    cache_filename = CACHE_DIR + cache_filename
    data = None    
    if not os.path.isfile(cache_filename):
        data = DatayesLocalFileMDProvider.get_data(trade_date, [sec_code])
        data = data.get(sec_code)
    if data is not None:
        with open(cache_filename, 'wb') as f:
            pickle.dump(data, f)
    else:
        with open(cache_filename, 'rb') as f:
            data = pickle.load(f)
    return data


def in_countinuous_auction(market_code, dt):
    """
    判断是否在集合竞价时间内,只用来判断tick内数据 !!!
    """
    hour = dt.hour
    min = dt.minute
    if hour == 9 and min < 30:
        return False
    if market_code == SZ_MARKET_CODE \
        and hour == 14 and min >= 57:
        return False
    return True


def cal_trade_time_seconds(t1, t2):
    if t1 >= t2:
        return -1 * cal_trade_time_seconds()
    if  (t1.hour < 12 and t2.hour < 12) or \
    (t1.hour > 12 and t2.hour > 12):
        return (t1-t2).total_seconds()
    t = datetime(t1.year, t1.month, t1.day, 11, 30)
    return (t - t1).total_seconds() + (t2 - t).total_seconds()


def cal_open_market_seconds(t):
    t_begin = datetime(t.year, t.month, t.day, 9, 30)
    return cal_trade_time_seconds(t_begin, t)


def cal_close_market_seconds(t):
    t_end = datetime(t.year, t.month, t.day, 15)
    return cal_trade_time_seconds(t, t_end)

    
    
    