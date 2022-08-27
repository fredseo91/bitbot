from lib import upbit_tool as ut
from lib import token_info
from lib import slack_msg as sl
import datetime
import time


UP = 1
DOWN = 0

invest_money = 6000

token_list = token_info.get_tokens()
access = token_list["access"]
secret = token_list["secret"]
slack_token = token_list["slack_token"]

slack = sl.slackbot("#bitbot", slack_token)
slack_sys = sl.slackbot("server-check", slack_token)

upbit_acc = ut.account(access, secret)
account_info = upbit_acc.get_upbit_account()




bot_dict = {
    "KRW-BTC" : ut.vol_breakout,
    "KRW-ETH" : ut.vol_breakout,
    "KRW-XRP" : ut.vol_breakout,
    "KRW-ADA" : ut.vol_breakout,
    "KRW-SOL" : ut.vol_breakout,

    "KRW-DOGE": ut.moving_average,
    "KRW-DOT" : ut.moving_average,
    "KRW-MATIC": ut.moving_average,
    "KRW-AVAX": ut.moving_average,
    "KRW-CHZ" : ut.moving_average,
}


slack.post_message("***bitbot initialized!***")

bot_list = list()

for coin in bot_dict:
    msg = (coin + " : " + bot_dict[coin].__name__)
    print(msg)
    slack.post_message(msg)
    bot_list.append(bot_dict[coin](coin, invest_money, account_info))


timecount_old = datetime.datetime.now()



while(1):
    bot_msg = list()

    for bot in bot_list:
        bot_msg.append(bot.loop())
        time.sleep(0.1)

    slack.msg_filter_post(bot_msg)


#--------------------------------------------#

    timecount_now = datetime.datetime.now()

    if timecount_now > timecount_old + datetime.timedelta(seconds = 10):
        slack_sys.post_message(timecount_now)
        timecount_old = timecount_now
