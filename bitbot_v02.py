from lib import util as ut
from lib import coin_graph as graph
from lib import control as ct
from lib import token_info

import datetime
import time


token_list = token_info.get_tokens()
access = token_list["access"]
secret = token_list["secret"]


test = ut.account(access, secret)



coin = ut.coin("KRW-AHT")
coin2 = ut.coin("KRW-ADA")
coin3 = ut.coin("KRW-ETC")


K = 0.7
min_krw = 10000 #5001 is too low

bot = ct.LW_strategy(coin, K)
bot2 = ct.LW_strategy(coin2, K)
bot3 = ct.LW_strategy(coin3, K)

while(1):
    bot.loop(min_krw)
    bot2.loop(min_krw)
    bot3.loop(min_krw)


    time.sleep(0.2)





print(LW.time_checker())
