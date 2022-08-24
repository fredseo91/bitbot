import pyupbit as pu
import time
import datetime

UP = 1
DOWN = 0


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

    def get_old_data(self, day_length):
        data =  pu.get_ohlcv(ticker=self.name, count = day_length)
        # datatemp =  pu.get_ohlcv(ticker=self.name, count = day_length)
        return data

    def update_df(self):
        temp = self.get_old_data(2)
        self.dataframe = temp.iloc[0,:]

    def day_over_check(self):
        time_tomorrow = (self.dataframe.name + datetime.timedelta(2))
        time_now = datetime.datetime.today() + datetime.timedelta(hours = 9)
        if (time_now >= time_tomorrow): #if the data is older than one day
            return UP #let the loop know!

        return DOWN


class vol_breakout(coin):

    def __init__(self, name, invest_money, K, upbit) :
        super().__init__(name, invest_money, upbit)
        time.sleep(0.5)
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
                self.recent_sell_info = self.sell_market_order(self.balance)
                self.recent_info = self.recent_sell_info
                return self.recent_info
            else :
                self.update_df()
                self.set_target_price()
                self.recent_info = "**target price set : " + self.name + "\nopen: " + str(self.open_price) + " | target: " + str(self.target_price)
                return self.recent_info

        else:
            if (self.current_price >= self.target_price and self.balance > 0):
                self.recent_buy_info = self.buy_market_order(self.invest_money)
                self.recent_info = self.recent_buy_info
                return self.recent_info

        return None


if __name__ == '__main__':


    upbit_acc = account(access,  secret)
    acc = upbit_acc.get_upbit_account()
    coin0 = vol_breakout("KRW-ETC", 10000, 0.5, acc)

    msg = coin0.loop()

    if msg != None:
        print(msg)
