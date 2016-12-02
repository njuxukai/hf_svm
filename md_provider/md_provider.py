# -*- coding: utf-8 -*- 

from abc import ABCMeta, abstractclassmethod


 
class MDProvider(metaclass=ABCMeta):
    @abstractclassmethod
    def  get_data(cls, trade_date, sec_codes):
        """
        {sec_code : data}
        data = {MarketData, OrderQueue, Transaction, Order(sz), IndexData(optional)}
        """
        pass