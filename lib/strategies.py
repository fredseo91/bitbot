import time
import datetime



UP = 1
DOWN = 0
INIT_FLAG = 0

class common:

    def __init__(self, coinbot, KRW):
        self.coinbot = coinbot
        self.KRW = KRW

    def get_current_price(self):
        self.current_price =  self.coinbot.get_current_price()

    def update_df(self):
        temp = self.coinbot.get_old_data(2) #one day old data
        self.dataframe = temp.iloc[0,:]

        # self.dataframe = self.coinbot.get_old_data(1) #one day old data


class moving_average(common):

    def __init__(self, coinbot, KRW):
        super().__init__(coinbot, KRW)

    def get_ma(self, day_length):
        df = self.coinbot.get_old_data(day_length)
        ma = df['close'].rolling(window = day_length, min_periods = 1).mean()
        #
        # dftemp = df.iloc[0,:]
        # print(dftemp)
        # print(dftemp.name)

        return ma


    # def gold_cross:
    ###buy when ma5 cross ma120 (upper),

    # def dead_cross:
    ###sell when ma60 cross ma120



class LW_strategy(common):
###########################################################################
#   methods in this class must report things in return to the host script #
#                                                                         #
#   set_target_price, buying, selling must report!                        #
###########################################################################


    def __init__(self, coinbot, KRW,  K):
        super().__init__(coinbot, KRW)
        self.K = K
        self.buyflag = DOWN


    def prv_init(self):
        time.sleep(0.02) #stablizer
        self.update_df()
        return self.set_target_price()


    def time_checker(self):

        time_tomorrow = (self.dataframe.name + datetime.timedelta(2)) #one day + old days

        time_now = datetime.datetime.today()

        if (time_now >= time_tomorrow): #if the data is older than one day
            return UP #let the loop know!

        return DOWN


    def set_target_price(self):
        high_price = self.dataframe['high']
        low_price = self.dataframe['low']
        close_price = self.dataframe['close']

        target_price =  close_price + (high_price - low_price) * self.K

        self.target_price = round(target_price,4) #dataframe type to number

        # ret_info = "***Target Price Set*** " + self.coinbot.name + " | HIGH:" + str(high_price) + " | LOW:" + str(low_price) + " | OPEN:" + str(close_price) + " | TARGET:" + str(self.target_price)
        ret_info = "**Target Price Set** " + self.coinbot.name + " | OPEN:" + str(close_price) + " | TARGET:" + str(self.target_price)
        return ret_info


    def loop(self):

        if(self.time_checker()): #시장마감 및 재시작.
            #SELL

            if(self.buyflag == UP): #if you bought anything,
                self.get_current_price() #get
                info = self.coinbot.sell_limit_order(self.current_price, self.buynumber) #sell everything with current price
                ret_info = self.coinbot.name + " | SELLING: " + str(info)
                if (info == None):
                    info = "sys fail"
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
            # if (1):
                self.buynumber = self.coinbot.get_purchase_number(self.KRW) #get # of coins with krw.
                info = self.coinbot.buy_limit_order(self.current_price, self.buynumber)

                # info = self.coinbot.buy_limit_order(0.01, 500100)
                # time.sleep(2)


                if (info == None):
                    info = "sys fail"

                ret_info = self.coinbot.name + " | BUYING: " + str(info)
                self.buyflag = UP

                # buy only once in a day
                return ret_info #report to the host

            return None
