from lib import upbit_tool as ut
from lib import token_info
from lib import slack_msg as sl
import datetime
import time


UP = 1
DOWN = 0

K = 0.5
invest_money = 7000

token_list = token_info.get_tokens()
access = token_list["access"]
secret = token_list["secret"]
slack_token = token_list["slack_token"]

slack = sl.slackbot("#bitbot", slack_token)
slack_sys = sl.slackbot("server-check", slack_token)

upbit_acc = ut.account(access, secret)
account_info = upbit_acc.get_upbit_account()

coin_name_list = ["KRW-ETC", "KRW-ADA", "KRW-XRP", "KRW-SOL", "KRW-ETH", "KRW-EOS, KRW-CHZ"]
coin_range = range(len(coin_name_list))
coin_list = list(coin_range)


bot_list = list(coin_range)
for i in coin_range:
    bot_list[i] = ut.vol_breakout(coin_name_list[i], invest_money, K, account_info )


slack.post_message("***bitbot initialized!***")

timecount_old = datetime.datetime.now()

while(1):
    bot_msg = list(coin_range)

    for i in coin_range:
        bot_msg[i] = bot_list[i].loop()
        time.sleep(0.1)


    slack.msg_filter_post(bot_msg)



#--------------------------------------------#

    timecount_now = datetime.datetime.now()

    if timecount_now > timecount_old + datetime.timedelta(seconds = 10):
        slack_sys.post_message(timecount_now)
        timecount_old = timecount_now
