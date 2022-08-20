from lib import upbit_tool as ut
from lib import coin_graph as graph
from lib import strategies
from lib import token_info
from lib import slack_msg as sl



import datetime
import time

UP = 1
DOWN = 0
INIT_FLAG = 0

K = 0.5
KRW = 10000 #5001 is too low



token_list = token_info.get_tokens()
access = token_list["access"]
secret = token_list["secret"]
slack_token = token_list["slack_token"]


slack = sl.slackbot("#bitbot", slack_token)
coins = ut.account(access, secret)
upbit_account = coins.get_upbit_account()

coin_name_list = ["KRW-ETC", "KRW-ADA", "KRW-XRP", "KRW-SOL", "KRW-CHZ"]

coin_range = range(len(coin_name_list))
coin_list = list(coin_range)

for i in coin_range:
    coin_list[i] = ut.coin(coin_name_list[i], upbit_account)






bot_list = list(coin_range)
for i in coin_range:
    bot_list[i] = strategies.LW_strategy(coin_list[i], KRW, K)
    



while(1):

    bot_msg = list(coin_range)

    if (INIT_FLAG == DOWN):
        INIT_FLAG = UP

        for i in coin_range:
            bot_msg[i] = bot_list[i].prv_init()
            time.sleep(0.05)


    else:
        for i in coin_range:
            bot_msg[i] = bot_list[i].loop()
            time.sleep(0.1)
            


    slack.msg_filter_post(bot_msg)

    time.sleep(1)
