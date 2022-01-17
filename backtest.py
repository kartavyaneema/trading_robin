import sys, getopt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from random import *
import matplotlib.animation as animation
from decimal import *
import json

from botchart import BotChart
from botstrategy import BotStrategy
import os

def main(argv):

	############### Delete old files
	# os.remove("./Data/stockPriceRecord.txt")
	# os.remove(".Data/moneyRecord.txt")
	# os.remove(".Data/tradeRecord.txt")

	backtest = True

	period = 300 # does not matter for backtest as period 
	exchange = "alpaca"
	orderSymbol = 'RCL'

	if exchange == 'binance':
		kline_interval = "5Min"  # make kline time same as ping interval
	elif exchange =='alpaca':
		kline_interval = '5Min'  ## 5Min, '1D'

	chart = BotChart(exchange =exchange, pair=orderSymbol, period=period, kline_interval=kline_interval, 
		startTime=1516064800, endTime=1516164800, backtest=backtest, numBins = 1000)

	strategy = BotStrategy(chart.client, exchange, orderSymbol, backtest=backtest, mockLive = False)  



	for candlestick in chart.getPoints():  # evaluating strategy with the chandle sticks
		strategy.tick(candlestick)

	# Closing logging File
	strategy.stockPriceRecord.close()
	strategy.moneyRecord.close()
	strategy.tradeRecord.close()




if __name__ == "__main__":
	main(sys.argv[1:])