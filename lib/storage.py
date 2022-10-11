# class vol_breakout(coin):
#
#     def __init__(self, name, invest_money, upbit) :
#         super().__init__(name, invest_money, upbit)
#         self.K = K
#
#         self.init_flag = DOWN
#
#     def set_target_price(self):
#
#         high_price = self.dataframe['high']
#         low_price = self.dataframe['low']
#         close_price = self.dataframe['close']
#
#         target_price =  close_price + (high_price - low_price) * self.K
#         self.open_price = close_price #for informational purpose
#         self.target_price = round(target_price,4) #dataframe type to number
#
#
#         # ret_info = "**Target Price Set** " + self.coinbot.name + " | OPEN:" + str(close_price) + " | TARGET:" + str(self.target_price)
#         # return ret_info
#
#     def loop(self):
#         #If event_flag is up, the main host will publish info to the user.
#         #and the main host will put the flag down after the publish.
#         self.get_balance()
#         self.get_current_price()
#
#         if (self.init_flag == DOWN):
#             self.init_flag = UP
#             self.update_df()
#             self.set_target_price()
#             self.recent_info = "**target price set : " + self.name + "\nopen: " + str(self.open_price) + " | target: " + str(self.target_price)
#             return self.recent_info
#
#
#         if (self.day_over_check()):
#             if (self.balance > 0):
#                 self.sell_in_process()
#                 return self.recent_info
#
#             else :
#                 self.update_df()
#                 self.set_target_price()
#                 self.recent_info = "**target price set : " + self.name + "\nopen: " + str(self.open_price) + " | target: " + str(self.target_price)
#                 return self.recent_info
#
#         else:
#             if (self.current_price >= self.target_price and self.balance == 0):
#                 self.buy_in_process()
#
#                 time.sleep(5) #not a right system.
#                 # when you buy stuff, need to have some time
#                 # before the purchase is done.
#                 # now, it's simply openloop time wait. need to change!
#
#                 # self.recent_info = self.recent_buy_info
#
#                 return self.recent_info
#
#         return None
