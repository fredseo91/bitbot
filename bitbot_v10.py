from lib import upbit_tool as ut
from lib import token_info
from lib import slack_msg as sl
from lib import moving_average as mv

import datetime
import time
import traceback

MODE = "REAL"
# MODE = "VIRTUAL"
UP = 1
DOWN = 0

invest_money = 6000

token_list = token_info.get_tokens()
access = token_list["access"]
secret = token_list["secret"]

slack_token = token_list["slack_token"]

slack = sl.slackbot("#bitbot", slack_token)
slack_sys = sl.slackbot("server-check", slack_token)

if MODE == "REAL":
    upbit_acc = ut.account(access, secret)
    account_info = upbit_acc.get_upbit_account()

elif MODE == "VIRTUAL":
    upbit_acc = ut.virtual_account(6000)
    account_info = upbit_acc.get_upbit_account()




bot_dict = {
    "KRW-BTC" : mv.moving_average,
    "KRW-ETH" : mv.moving_average,
    "KRW-XRP" : mv.moving_average,
    "KRW-ADA" : mv.moving_average,
    "KRW-SOL" : mv.moving_average,

    "KRW-DOGE": mv.moving_average,
    "KRW-DOT" : mv.moving_average,
    "KRW-MATIC": mv.moving_average,
    "KRW-AVAX": mv.moving_average,
    "KRW-CHZ" : mv.moving_average,
}


slack.post_message_print("***bitbot initialized!***")

bot_list = list()
msg_total = ""
for coin in bot_dict:
    msg = (coin + " : " + bot_dict[coin].__name__)
    msg_total = msg_total + "\n" + msg
    bot_list.append(bot_dict[coin](coin, invest_money, account_info))
slack.post_message_print(msg_total)


timecount_old = datetime.datetime.now()



while(1):
    try:

        bot_msg = list()

        for bot in bot_list:
            bot_msg.append(bot.loop())
            time.sleep(0.05)

        slack.msg_filter_post(bot_msg)


    except Exception:
        err = traceback.format_exc()
        print(err)
        slack.post_message(err)


    #--------------------------------------------#
    finally:
        timecount_now = datetime.datetime.now()

        if timecount_now > timecount_old + datetime.timedelta(seconds = 0.1):
            slack_sys.post_message(timecount_now)
            timecount_old = timecount_now
