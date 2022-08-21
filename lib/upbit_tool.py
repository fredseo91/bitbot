import pyupbit as pu


#need to fix the structure

class account():


    def __init__(self, access, secret):

        self.access = access
        self.secret = secret
        self.upbit = pu.Upbit(self.access, self.secret)

    def get_upbit_account(self):
        return self.upbit

class coin(account):

    def __init__(self,name, upbit):
        self.name = name
        self.upbit = upbit

    def get_balance(self):
        return self.upbit.get_balance(self.name)

    def get_current_price(self):
        return float(pu.get_current_price(self.name))

    def get_current_balance(self):
        return self.get_my_balance(self.name)

    def get_minimum_purchase_number(self):
        return (5001 / self.get_current_price())

    def get_purchase_number(self, money):
        return (money / self.get_current_price())

    def buy_limit_order(self, price, number):
        buy_info = self.upbit.buy_limit_order(self.name, price, number)
        return buy_info

    def sell_limit_order(self, price, num):
        sell_info = self.upbit.sell_limit_order(self.name, price, num)
        return sell_info

    def cancel_order(self, order_info):
        cancel_info = self.upbit.cancel_order(order_info['uuid'])

    def get_old_data(self, day_length):
        data =  pu.get_ohlcv(ticker=self.name, count = day_length)
        # datatemp =  pu.get_ohlcv(ticker=self.name, count = day_length)
        return data



if __name__ == '__main__':


    test = account()
    print(test.get_my_balance("KRW-AHT"))

    aht = coin("KRW-AHT")

    print(aht.get_current_price())
