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
import csv

def main(orderSymbol):

	backtest = True

	period = 300 # does not matter for backtest as period 
	exchange = "alpaca"
	
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

	with open('sp500.csv', newline='') as f:
		reader = csv.reader(f)
		data = list(reader)

	# data = ['AGNC', 'AMC', 'AMZN', 'CCL', 'CMI', 'CIM', 'DDD', 'EPR', 'MEDS', 'MSFT', 'PFE', 'SAVA', 'TSLA' ]

	for i in data:
		orderSymbol = i[0]
		print(i)
		main(orderSymbol)