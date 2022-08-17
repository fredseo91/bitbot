import time
import datetime




class LW_strategy():



    def __init__(self,  coinbot, K):
        self.coinbot = coinbot
        self.buyflag = 0
        self.dataframe = self.coinbot.get_old_data(1)
        self.K = K
        self.set_target_price = self.set_target_price()
        self.current_price = 0
        self.old_price = 0

    def update_df(self):
        self.dataframe = self.coinbot.get_old_data(1)
        return self.dataframe
        # self.dataframe = dataframe


    def time_checker(self):
        old = self.dataframe.index + datetime.timedelta(1)
        old = old[0]
        now = datetime.datetime.today()
        if (now >= old):
            return 1 #DATAFRAME NEEDS TO BE CHANGED NOW
        else:
            return 0

    def set_target_price(self):
        high_price_yesterday = self.dataframe['high']
        low_price_yesterday = self.dataframe['low']
        open_price_today = self.dataframe['close']

        target_price =  open_price_today + (high_price_yesterday - low_price_yesterday) * K


        self.high_price = high_price_yesterday[0]
        self.low_price = low_price_yesterday[0]
        self.target_price = target_price[0]

        print(self.coinbot.name, "HIGH:", self.high_price, "LOW:", self.low_price,
        "OPEN:", open_price_today[0], "TARGET:", self.target_price)

        return self.target_price

    def price_check(self):

        self.current_price =  self.coinbot.get_current_price()
        return self.current_price

    


    def loop(self, money):


        if(self.time_checker()): #시장마감 및 재시작.
            #SELL
            if(self.buyflag == 1):
                price = self.price_check()
                info = self.coinbot.sell_limit_order(price, self.buynumber)
                print(self.coinbot.name, "SELLING: ", info)
                self.buyflag = 0
                #sell all

            self.update_df()
            self.set_target_price()

        else:

            self.old_price = self.current_price
            price = self.price_check()

            if (self.old_price != price):
                print(self.coinbot.name, "PRICE:", price)

            if (price >= self.target_price and self.buyflag == 0):
                self.buynumber = self.coinbot.get_purchase_number(money)
                info = self.coinbot.buy_limit_order(price, self.buynumber)
                print(self.coinbot.name, "BUYING: ", info)
                self.buyflag = 1
                # buy only once in a day
