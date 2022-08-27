import pyupbit as pu
import time
import datetime
import pandas

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

class coin(account):

    def __init__(self, name, invest_money, upbit):
        self.name = name
        self.upbit = upbit
        self.invest_money = invest_money
        self.event_flag = DOWN


    def get_balance(self):
        self.balance = self.upbit.get_balance(self.name)

    def get_current_price(self):
        self.current_price = float(pu.get_current_price(self.name))
        return self.current_price

    def get_minimum_purchase_number(self):
        return (5001 / self.get_current_price())

    def get_purchase_number(self, money):
        return (money / self.get_current_price())

    def buy_limit_order(self, price, number):
        buy_info = self.upbit.buy_limit_order(self.name, price, number)
        return buy_info

    def buy_market_order(self, price):
        buy_info = self.upbit.buy_market_order(self.name, price)
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
        time_now = datetime.datetime.today() + datetime.timedelta(hours = 9)
        # time_now = datetime.datetime.today() #for local pc

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




class vol_breakout(coin):

    def __init__(self, name, invest_money, upbit) :
        super().__init__(name, invest_money, upbit)
        self.K = K

        self.init_flag = DOWN

    def set_target_price(self):

        high_price = self.dataframe['high']
        low_price = self.dataframe['low']
        close_price = self.dataframe['close']

        target_price =  close_price + (high_price - low_price) * self.K
        self.open_price = close_price #for informational purpose
        self.target_price = round(target_price,4) #dataframe type to number


        # ret_info = "**Target Price Set** " + self.coinbot.name + " | OPEN:" + str(close_price) + " | TARGET:" + str(self.target_price)
        # return ret_info

    def loop(self):
        #If event_flag is up, the main host will publish info to the user.
        #and the main host will put the flag down after the publish.
        self.get_balance()
        self.get_current_price()

        if (self.init_flag == DOWN):
            self.init_flag = UP
            self.update_df()
            self.set_target_price()
            self.recent_info = "**target price set : " + self.name + "\nopen: " + str(self.open_price) + " | target: " + str(self.target_price)
            return self.recent_info


        if (self.day_over_check()):
            if (self.balance > 0):
                self.recent_sell_info = self.sell_limit_order(self.current_price, self.balance)
                self.recent_info = self.uuid_decompose(self.recent_sell_info['uuid'])
                return self.recent_info

            else :
                self.update_df()
                self.set_target_price()
                self.recent_info = "**target price set : " + self.name + "\nopen: " + str(self.open_price) + " | target: " + str(self.target_price)
                return self.recent_info

        else:
            if (self.current_price >= self.target_price and self.balance == 0):
                self.purchase_num = self.get_purchase_number(self.invest_money)
                self.recent_buy_info = self.buy_limit_order(self.current_price, self.purchase_num)
                self.recent_info = self.uuid_decompose(self.recent_buy_info['uuid'])

                time.sleep(5) #not a right system.
                # when you buy stuff, need to have some time
                # before the purchase is done.
                # now, it's simply openloop time wait. need to change!

                # self.recent_info = self.recent_buy_info

                return self.recent_info

        return None

class moving_average(coin):

    def __init__(self, name, invest_money, upbit) :
        super().__init__(name, invest_money, upbit)

        self.init_flag = DOWN

    def get_df(self, max_length, type):
        self.df = self.get_old_data(max_length, type)


    def get_ma(self, length):
        old_ma = self.df['close'].rolling(window = length, min_periods = 1).mean().iloc[-2]
        new_ma = self.df['close'].rolling(window = length, min_periods = 1).mean().iloc[-1]
        return new_ma, old_ma

    def cross_detection(self, ma_1_length, ma_2_length):
        ma_1_new, ma_1_old = self.get_ma(ma_1_length)
        ma_2_new, ma_2_old = self.get_ma(ma_2_length)
        #ma_1 : smaller number
        #ma_2 : bigger number

        # if old compare is negative,
        # it might get into "golden cross"

        # if old compare is positive,
        # it might get into "dead cross"

        old_compare = ma_1_old - ma_2_old
        new_compare = ma_1_new - ma_2_new

        if (old_compare < 0 and new_compare >= 0):
            self.state = "golden cross"
        elif (old_compare > 0 and new_compare <= 0):
            self.state = "dead cross"
        elif (new_compare > 0):
            self.state = "up state"
        elif (new_compare < 0):
            self.state = "down state"
        else:
            self.state = "none"

        return self.state



    def loop(self):
        self.get_balance()
        self.get_current_price()

        self.get_df(100, "minute5")
        self.cross_detection(5,20)
        #temp algorithm

        if (self.state == "golden cross" and self.balance == 0):
            self.purchase_num = self.get_purchase_number(self.invest_money)
            self.recent_buy_info = self.buy_limit_order(self.current_price, self.purchase_num)
            self.recent_info = self.uuid_decompose(self.recent_buy_info['uuid'])

            time.sleep(5) #not a right system.
            # when you buy stuff, need to have some time
            # before the purchase is done.
            # now, it's simply openloop time wait. need to change!

            # self.recent_info = self.recent_buy_info

            return self.recent_info


        elif (self.state == "dead cross" and self.balance > 0):

            self.recent_buy_info = self.sell_limit_order(self.current_price, self.balance)
            self.recent_info = self.uuid_decompose(self.recent_sell_info['uuid'])

            return self.recent_info


        else:
            return None






if __name__ == '__main__':


    upbit_acc = account(access,  secret)
    acc = upbit_acc.get_upbit_account()
    coin0 = moving_average("KRW-ETC", 10000,  acc)


    coin0.get_df(10, "minute5")

    msg = coin0.cross_detection(5,20)


    print(msg)
