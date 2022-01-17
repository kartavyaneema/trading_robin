import sys, getopt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from random import *
import matplotlib.animation as animation

from binance.client import Client


api_key = 'bY6fWXedeXh2LIWUrFlOHPzQtBUPYZIoKGGapD3Rzc65V5VfadxOrGp0KzABZe2W' # Please write your key
api_secret = 'QXYKUd5sg5tpJDNfIbb9uek71noSpFdS134GPHxDZm3fOkFouWm9ldnjjC3ItSPh' # Please write your key
client = Client(api_key, api_secret)


orderSymbol = 'BTCUSDT'
num_stock = 0.001103
# tempResult = client.create_order(symbol=orderSymbol, side='BUY', \
# 							 type='MARKET', quantity=num_stock)
# print('TR ', tempResult)

# orderID = tempResult['orderId']

# tempStatus = client.get_order(symbol=orderSymbol,orderId=orderID)
# print('ts ', tempStatus)

recent_trade_temp = client.get_recent_trades(symbol=orderSymbol,limit=1)
# exitPrice = float(recent_trade_temp['price'])

print('ts p ' , recent_trade_temp)
print('ts p ' , recent_trade_temp[0]['price'])
print('ts ty ' , type(recent_trade_temp[0]['price']))
print('ts tyo ' , float(recent_trade_temp[0]['price']))
 
