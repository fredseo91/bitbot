import time
import datetime
import pandas
import os
import numpy as np
import matplotlib.pyplot as plt

from lib import token_info
from lib import moving_average
from lib import upbit_tool as ut

UP = 1
DOWN = 0

invest_money = 6000

token_list = token_info.get_tokens()
access = token_list["access"]
secret = token_list["secret"]

upbit_acc = ut.account(access, secret)
account_info = upbit_acc.get_upbit_account()





if __name__ == '__main__':
