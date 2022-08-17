
from . import token_info as tk

import pyupbit as pu
import time
import pandas as pd
import datetime


list_of_all = ""
today = datetime.datetime.today()

class coins:

    upbit = pu.Upbit(tk.access, tk.secret)
    balance_list = ""


    def __init__(self):
        self = self

    def update_infos(self):
        global list_of_all
        list_of_all = self.upbit.get_balances()
        return list_of_all


class coin(coins) :


    def __init__(self, name):
        self.name = name


    def update_my_info(self):
        self.get_my_info()
        self.price_now = self.get_price_now()
        self.min_buynum = self.get_min_buynum()


    def get_price_now(self):
        return float(pu.get_current_price(self.name))


    def get_my_info(self):

        search_name = self.name[4:]

        for i in range(len(list_of_all)):
            if (search_name == list_of_all[i]['currency']):
                self.dict = list_of_all[i]

        self.balance = float(self.dict['balance']) #num of coins
        self.avg_buy_price = float(self.dict['avg_buy_price'])
        self.purchase_value = float(self.balance) * float(self.avg_buy_price)



    def get_min_buynum(self) :

        #5000won is minimum purchase money
        #5000won / the current price
        return  ( 5001 / self.price_now )



    def buy_limit_order(self, price, num):

        self.recent_buy = self.upbit.buy_limit_order(self.name, price, num)
        return self.recent_buy

    def sell_limit_order(self, price, num):
        self.upbit.sell_limit_order(self.name, price, num)

    def order_monitor(self):

        print(self.upbit.get_order(self.name))



        # this is a temporary method



        # self.uuid_temp = self.upbit.get_order(self.recent_buy['uuid'])
        # print(self.uuid_temp)
        # ret = upbit.get_order("KRW-BTC") # 미체결 주문
        # ret = upbit.get_order("KRW-BTC", state="done") # 완료된 주문
        # ret = upbit.get_order("UUID") # 특정 주문 상세 조회


    def cancel_order(self):
        #need to fix!

        self.upbit.cancel_order(self.recent_buy['uuid'])



    def get_old_exchange_data(self):
        self.old_exchange_data = pu.get_ohlcv(ticker=self.name)
        self.old_exchange_length = len(self.old_exchange_data.index)

        # self.data_1day_ago = self.old_exchange_data[length-1:length]
        # self.data_1week_ago = self.old_exchange_data[length-7:length]
        # self.data_2weeks_ago = self.old_exchange_data[length-14:length]
        # self.data_4weeks_ago = self.old_exchange_data[length-28:length]
        return self.old_exchange_data


    def average_data(self, daylength, type):
        #type : open, high, low, close, volume, value
        length = self.old_exchange_length
        dataframe = self.old_exchange_data[length-daylength:length]
        return sum(dataframe[type] / len(dataframe))


    #
    # def moving_average(self, daylength):
    #
    #     length = self.old_exchange_length
    #     dataframe = self.old_exchange_data[length-daylength:length]
    #
    #




# {'uuid': '0ac8ac6f-8206-407d-9a90-814d89433c7e',
# 'side': 'bid', 'ord_type': 'limit', 'price': '0.001',
# 'state': 'wait', 'market': 'KRW-AHT', 'created_at': '2022-08-11T01:19:21+09:00',
# 'volume': '5000000.0', 'remaining_volume': '5000000.0', 'reserved_fee': '2.5',
# 'remaining_fee': '2.5', 'paid_fee': '0.0', 'locked': '5002.5', 'executed_volume': '0.0', 'trades_count': 0}







if __name__ == '__main__':

    mycoins = coins()
    list_of_all = mycoins.update_infos() #global function


    AHT = coin("KRW-AHT")
    AHT.update_my_info()
    AHT.get_old_exchange_data()
    AHT.analyze_old_data(AHT.data_4weeks_ago)
    # print(today)





    # print(AHT.dict)
