from . import upbit_tool as up
import time

UP = 1
DOWN = 0




class moving_average(up.coin):

    def __init__(self, name, invest_money, upbit) :
        super().__init__(name, invest_money, upbit)

        self.init_flag = DOWN
        self.fsm_state = 'init'

    def get_df(self, max_length, type):
        self.df = self.get_old_data(max_length, type)


    def get_ma(self, length):
        old_ma = self.df['close'].rolling(window = length, min_periods = 1).mean().iloc[-2]
        new_ma = self.df['close'].rolling(window = length, min_periods = 1).mean().iloc[-1]
        return new_ma, old_ma

    def get_ema(self, length):
        old_ema = self.df['close'].ewm(length).mean().iloc[-2]
        new_ema = self.df['close'].ewm(length).mean().iloc[-1]

        return new_ema, old_ema

    def cross_detection(self, ma_1_length, ma_2_length):
        self.get_df(50, "minute15") # parameters....!

        ma_1_new, ma_1_old = self.get_ema(ma_1_length)
        ma_2_new, ma_2_old = self.get_ema(ma_2_length)
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
        #finite state machine


        return self.fsm_dict[self.fsm_state]['func_name'](self)
        # print(self.name, self.fsm_state)



    def fsm_init(self):
        self.fsm_testing(True)
        return None


    def fsm_check_balance(self):
        self.get_balance()
        test = (self.balance > 0)
        self.fsm_testing(test)
        if test == True:
            msg = self.name + " balance : " + str(self.balance)
            return msg
        else:
            return None

    def fsm_wait_goldencross(self):
        self.cross_detection(5,20)
        test = (self.state == 'golden cross')
        self.fsm_testing(test)
        if test == True:
            msg = self.name + " : golden cross detected"
            return msg
        else:
            return None

    def fsm_buy_coins(self):
        self.buy_in_process()
        self.fsm_testing(True) #there is no test.
        # msg = self.name + "| buying at price of : " + str(self.current_price)
        return self.recent_buy_info


    def fsm_wait_for_bought(self):
        info = self.upbit.get_order(self.name, state = 'wait')
        test = (info == [])
        self.fsm_testing(test)

        return None


    def fsm_wait_deadcross(self):
        self.cross_detection(5,20)
        test = (self.state == 'dead cross')
        self.fsm_testing(test)

        if test == True:
            msg = self.name + " : dead cross detected"
            return msg
        else:
            return None



    def fsm_sell_coins(self):
        self.get_current_price()
        if (self.current_price < self.invest_money):
            self.fsm_state = 'wait_deadcross'
            msg = "the price is lower than invested. keep waiting."
            return msg
        else:
            info =  self.sell_in_process()
            self.fsm_testing(True)
            # msg = self.name + "| selling at price of : " + str(self.current_price)
            return self.recent_sell_info


    def fsm_wait_for_sold(self):
        info = self.upbit.get_order(self.name, state = 'wait')
        test = (info == [])
        self.fsm_testing(test)
        return None


    def fsm_testing(self, test):
        if test:
            self.fsm_state = self.fsm_dict[self.fsm_state]['true']
        else :
            self.fsm_state = self.fsm_dict[self.fsm_state]['false']









    fsm_dict = {
        # function name, function true, function false

        'init' : {'func_name' : fsm_init, 'true' : 'check_balance', 'false' : 'check_balance'},

        'check_balance' : {'func_name' : fsm_check_balance, 'true' : 'wait_deadcross', 'false' : 'wait_goldencross'},
        'wait_goldencross' : {'func_name' : fsm_wait_goldencross, 'true' : 'buy_coins', 'false' : 'wait_goldencross'},
        'buy_coins' : {'func_name' : fsm_buy_coins, 'true' : 'wait_for_bought', 'false' : 'wait_for_bought'},
        'wait_for_bought' : {'func_name' : fsm_wait_for_bought, 'true' : 'wait_deadcross', 'false' : 'wait_for_bought'},
        'wait_deadcross' : {'func_name' : fsm_wait_deadcross, 'true' : 'sell_coins', 'false' : 'wait_deadcross'},
        'sell_coins' : {'func_name' : fsm_sell_coins, 'true' : 'wait_for_sold', 'false' : 'wait_for_sold'},
        'wait_for_sold' : {'func_name' : fsm_wait_for_sold, 'true' : 'check_balance', 'false' : 'wait_for_sold'}



        # state machine structure
        # 1. init : set up variables and do checkups <- removed. not necessary
        # 2. check balance : check if there is balance. if not, wait for golden cross
        # 3. wait_for_golden cross: if golden cross, buy coins.
        # 4. wait for purchase done. if purchase is done, wait for dead cross to sell.
        # 5. sell if dead cross. wait for purchase done.
        # if sold, go to number 2.

    }


if __name__ == '__main__':

    upbit = up.account(access,  secret)
    acc = upbit.get_upbit_account()
    coin0 = moving_average("KRW-ADA", 7000,  acc)

    while(1):
        coin0.loop()
        print(coin0.fsm_state)
        time.sleep(0.1)
