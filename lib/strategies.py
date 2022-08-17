import time
import datetime



UP = 1
DOWN = 0
INIT_FLAG = 0


class LW_strategy():
###########################################################################
#   methods in this class must report things in return to the host script #
#                                                                         #
#   set_target_price, buying, selling must report!                        #
###########################################################################


    def __init__(self,  coinbot, K, MIN_KRW):
        self.coinbot = coinbot
        self.K = K
        self.MIN_KRW = MIN_KRW
        self.buyflag = DOWN


    def prv_init(self):
            time.sleep(0.02) #stablizer
            self.update_df()
            return self.set_target_price()




    def update_df(self):
        self.dataframe = self.coinbot.get_old_data(1) #one day old data

    def get_current_price(self):
        self.current_price =  self.coinbot.get_current_price()


    def time_checker(self):
        time_tomorrow = (self.dataframe.index + datetime.timedelta(1))[0] #one day
        time_now = datetime.datetime.today()

        if (time_now >= time_tomorrow): #if the data is older than one day
            return UP #let the loop know!

        return DOWN




    def set_target_price(self):
        high_price = self.dataframe['high']
        low_price = self.dataframe['low']
        close_price = self.dataframe['close']

        target_price =  close_price + (high_price - low_price) * self.K

        self.target_price = round(target_price[0],4) #dataframe type to number

        # ret_info = "***Target Price Set*** " + self.coinbot.name + " | HIGH:" + str(high_price[0]) + " | LOW:" + str(low_price[0]) + " | OPEN:" + str(close_price[0]) + " | TARGET:" + str(self.target_price)
        ret_info = "**Target Price Set** " + self.coinbot.name + " | OPEN:" + str(close_price[0]) + " | TARGET:" + str(self.target_price)

        return ret_info









    def loop(self):



        if(self.time_checker()): #시장마감 및 재시작.
            #SELL

            if(self.buyflag == UP): #if you bought anything,
                self.get_current_price() #get
                info = self.coinbot.sell_limit_order(self.current_price, self.buynumber) #sell everything with current price
                ret_info = self.coinbot.name + " | SELLING: " + info
                self.buyflag = DOWN

                return ret_info #report to the host

            elif (self.buyflag == DOWN):

                # either way, update dataframe and reset target_price
                self.update_df()
                ret_info = self.set_target_price()

                return ret_info #report to the host



        else:

            self.get_current_price()

            if (self.current_price >= self.target_price and self.buyflag == DOWN):

                self.buynumber = self.coinbot.get_purchase_number(self.MIN_KRW) #get # of coins with krw.
                info = self.coinbot.buy_limit_order(self.current_price, self.buynumber)

                if (info == None):
                    info = "sys fail"

                ret_info = self.coinbot.name + " | BUYING: " + info
                self.buyflag = UP

                # buy only once in a day
                return ret_info #report to the host

            return None
