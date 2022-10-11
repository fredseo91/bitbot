import pyupbit as pu
import time
import datetime
import pandas
import os

# import moving_average as mv

UP = 1
DOWN = 0
K = 0.5
#need to fix the structure

class account():


    def __init__(self, access, secret):

        self.access = access
        self.secret = secret
        self.upbit = pu.Upbit(self.access, self.secret)


    def get_upbit_account(self):
        return self.upbit

class virtual_account():
    def __init__(self, wallet):
        self.balance = 0
        self.wallet = wallet

    def get_upbit_account(self):
        return self


    def get_balance(self, name):
        return self.balance

    def prv_get_current_price(self, name):
        return float(pu.get_current_price(name))

    def buy_limit_order(self, name, price, number):
        purchased = price*number
        spent = price*1.0005 * number
        self.wallet -= spent
        self.balance += purchased
        msg = name + " | purhcased : " + purchased
        return msg

    def buy_market_order(self, name, money):
        price = self.prv_get_current_price(name)
        number = money / price

        spent = price*1.0005 * number
        self.wallet -= spent
        self.balance += purchased
        msg = name + " | purhcased : " + purchased
        return msg

    def sell_limit_order(self, name, price, num):
        sold = price*number
        earned = price*0.9995 * number
        self.wallet += earned
        self.balance -= sold
        msg = name + " | sold : " + purchased
        return msg

    def sell_market_order(self, name, money):
        price = self.prv_get_current_price(name)
        number = money / price

        sold = price*number
        earned = price*0.9995 * number
        self.wallet += earned
        self.balance -= sold
        msg = name + " | sold : " + purchased
        return msg

    def get_order(self, uiud):
        return []

class coin(account):

    def __init__(self, name, invest_money, upbit):
        self.name = name
        self.upbit = upbit
        self.invest_money = invest_money
        self.event_flag = DOWN
        self.user = os.getlogin()


    def get_balance(self):
        self.balance = self.upbit.get_balance(self.name)
        return self.balance

    def get_current_price(self):
        self.current_price = float(pu.get_current_price(self.name))
        return self.current_price

    def get_purchase_number(self, money):
        return (money / self.get_current_price())

    def buy_limit_order(self, price, number):
        buy_info = self.upbit.buy_limit_order(self.name, price, number)
        return buy_info

    def buy_market_order(self, money):
        buy_info = self.upbit.buy_market_order(self.name, money)
        return buy_info

    def sell_limit_order(self, price, num):
        sell_info = self.upbit.sell_limit_order(self.name, price, num)
        return sell_info

    def sell_market_order(self, num):
        sell_info = self.upbit.sell_market_order(self.name, num)
        return sell_info

    def get_order_info(self, uuid):
        order_info = self.upbit.get_order(uuid)
        return order_info

    def cancel_order(self, order_info):
        cancel_info = self.upbit.cancel_order(order_info['uuid'])

    def get_old_data(self, length, type):
        data =  pu.get_ohlcv(ticker=self.name, count = length, interval = type)
        #type : day = 일봉, minute1 = 1분봉, minute3 = 3분봉, minute5 = 5분봉 , minute10 = 10분봉
        #minute15 = 15분봉, minute30 = 30분봉, minute60 = 60분봉, minute240 = 240분봉
        #week = 주봉, month = 월봉

        return data

    def update_df(self):
        temp = self.get_old_data(2, "day")
        self.dataframe = temp.iloc[0,:]

    def day_over_check(self):
        time_tomorrow = (self.dataframe.name + datetime.timedelta(2))
        if (self.user == jseo):
            time_now = datetime.datetime.today() #for local pc
        else:
            time_now = datetime.datetime.today() + datetime.timedelta(hours = 9)

        if (time_now >= time_tomorrow): #if the data is older than one day
            return UP #let the loop know!

        return DOWN

    def uuid_decompose(self, uuid):
        info = self.get_order_info(uuid)
        info_uuid = uuid
        if (info['side'] == 'bid'):
            info_side = 'buying'
        else :
            info_side = 'selling'

        total_info =  info_side + " : " + self.name + "\nprice: " + info['price'] + " | volume : " + info['volume']

        return total_info


    def buy_in_process(self):
        self.get_current_price()
        self.purchase_num = self.get_purchase_number(self.invest_money)
        self.recent_buy_info = self.buy_limit_order(self.current_price, self.purchase_num)
        self.purchased_price = self.current_price
        # self.recent_buy_info = self.buy_market_order(self.invest_money)

    def sell_in_process(self):
        self.get_current_price()
        self.get_balance() #user may have bought some manually.
        self.recent_sell_info = self.sell_limit_order(self.current_price, self.balance)


        # self.recent_sell_info = self.sell_market_order(self.balance)







if __name__ == '__main__':

    upbit_acc = account(access,  secret)
    acc = upbit_acc.get_upbit_account()
    # coin0 = moving_average("KRW-ADA", 7000,  acc)

    coin = mv.moving_average("KRW-ADA", 6000, acc)
    print(coin.get_balances())

    #
    # while(1):
    #     coin0.loop()
    #     time.sleep(0.1)
    #
    #

    # vir = virtual_account(6000)
    # acc = vir.get_upbit_account()

    # print(acc.get_balance(""))









#get order, done info : {'uuid': '6e42a2e9-6db8-42a5-89e0-cae94b1d8063', 'side': 'bid', 'ord_type': 'limit', 'price': '57300', 'state': 'done', 'market': 'KRW-ETC', 'created_at': '2022-08-15T10:11:35+09:00', 'volume': '0.08727748', 'remaining_volume': '0', 'reserved_fee': '2.500499802', 'remaining_fee': '0', 'paid_fee': '2.500499802', 'locked': '0', 'executed_volume': '0.08727748', 'trades_count': 1}]
