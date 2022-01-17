import sys, getopt
import time
from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick
import csv
import urllib.error
import json
from datetime import date
import os
from datetime import datetime


class BotAsset(object):
	def __init__(self, orderSymbol = 'MSFT', period = 300, exchange = "alpaca", kline_interval = "5Min", moneyPerTrade = 100,mockLive = False ):

		self.orderSymbol = orderSymbol
		self.period = period
		self.exchange = exchange
		self.kline_interval = kline_interval
		self.moneyPerTrade = moneyPerTrade
		self.chart = BotChart(exchange = self.exchange, pair=self.orderSymbol, period=self.period,\
							 kline_interval=self.kline_interval, backtest=False)

		self.strategy = BotStrategy(self.chart.client, exchange = self.exchange, orderSymbol = self.orderSymbol,\
									 backtest=False, mockLive = mockLive, equity_money = 0, cash = self.moneyPerTrade)

		
	def tick(self):
		a = 1


########################################################
######################## Main Function##################
########################################################

def main(period = 300, exchange = "alpaca", kline_interval = "5Min", moneyPerTrade = 100, \
	    maxNumTrades = 10, numPreviousCandleStick = 100, maxPingPerDay = 75, mockLive = False):
	
	period = period
	exchange = exchange
	kline_interval = kline_interval
	moneyPerTrade = moneyPerTrade

	# with open('sp500.csv', newline='') as f:
	# 	reader = csv.reader(f)
	# 	data = list(reader)

	data = [['MSFT'], ['TSLA'], ['FB'], ['PLUG'], ['AMZN'], \
			['GOOG'], ['NVDA'], ['V'], ['DIS'], ['CSCO'], \
			['BA'], ['TJX'], ['CCI'], ['CMG'], ['ZBRA'], \
			['VIAC'], ['GRMN'], ['HOLX'], ['MRO'], ['JNPR'],\
			['FOX'], ['DISCA'], ['UAA'], ['NOV'], ['LEG']]

	########################################S
	###### Create Object list for each symbol
	########################################
	asset = []
	for i in data:
		orderSymbol = i[0]
		# print(i[0])
		asset.append(BotAsset(orderSymbol = orderSymbol, period = period, exchange = exchange, \
			 kline_interval = kline_interval, moneyPerTrade = moneyPerTrade, mockLive = mockLive))

	########################################
	###### Get the data for past 100 candlestick and put in botstrategy
	########################################
	for tempAsset in asset:
		data = tempAsset.chart.getPreviousCandleStick(numPreviousCandleStick = numPreviousCandleStick)
		for i in data:
			tempAsset.strategy.tick(i, evaluateTradingOptions = False)

	########################################
	########## Go Live ##
	########################################
	print('Sleeping for period after downloading the data')
	# time.sleep(int(period))  ### Sleep for 5 mins

	if time.time() % period > 60:
		time.sleep(period + 60 - time.time() % period)
	else:
		time.sleep(60 - time.time() % period)
	
	counter = 0
	numOpenTrades = 0

	while counter <= maxPingPerDay:
		print('counter: ', counter)
		for tempAsset in asset:
			########################### Get the CandleStick Data
			try:
				if exchange == 'alpaca' or exchange == "binance":
					print('OrderSymbol: ', tempAsset.orderSymbol)
					developingCandlestick = tempAsset.chart.getCandleStick()  # Will directly return a candlestick object: to reduce number of ping
				else:
					developingCandlestick = tempAsset.chart.getCandleStick()
					
			except urllib.error.URLError:
				print('error handed this time ')
				time.sleep(int(2))
				if exchange == 'alpaca' or exchange == "binance":
					developingCandlestick = tempAsset.chart.getCandleStick()  # Will directly return a candlestick object: to reduce number of ping
				else:
					developingCandlestick = tempAsset.chart.getCandleStick()
					
			############################ Make trade if we can
			numTrades_before = len(tempAsset.strategy.trades)
			if (numOpenTrades <maxNumTrades) and numTrades_before == 0:			
				tempAsset.strategy.tick(developingCandlestick)
			else:
				tempAsset.strategy.tick(developingCandlestick, evaluateOnlySell = True)

			numTrades_after = len(tempAsset.strategy.trades)

			###################### Update Number of open trades
			if numTrades_before == 1 and numTrades_after == 0:  ## recently sold
				numOpenTrades = numOpenTrades - 1
			elif numTrades_before == 0 and numTrades_after == 1: ## recently bought
				numOpenTrades = numOpenTrades + 1

		print('Sleeping for period after getting the candlestick')
		now = datetime.now()
		current_time = now.strftime("%H:%M:%S")
		print("Current Time =", current_time)

		# time.sleep(int(period))  ### Sleep for 5 mins
		if time.time() % period > 60:
			time.sleep(period + 60 - time.time() % period)
		else:
			time.sleep(60 - time.time() % period)
			
		counter = counter + 1

	
	########################################
	########## Save Data
	########################################

	today = date.today()
	d1 = today.strftime("%d_%m_%Y")
	if not os.path.exists('./Data/'+ d1):
		os.makedirs('./Data/'+ d1)

	for tempAsset in asset:


		fileName = './Data/'+ d1+ '/' + tempAsset.orderSymbol + '_stockPriceRecord.json'
		jsonFile = open(fileName, "w")
		jsonString = json.dumps(tempAsset.strategy.stockPriceRecord)
		jsonFile.write(jsonString)
		jsonFile.close()

		fileName = './Data/'+ d1+ '/' + tempAsset.orderSymbol + '_tradeRecord.json'
		jsonFile = open(fileName, "w")
		jsonString = json.dumps(tempAsset.strategy.tradeRecord)
		jsonFile.write(jsonString)
		jsonFile.close()

		fileName = './Data/'+ d1+ '/' + tempAsset.orderSymbol + '_moneyRecord.json'
		jsonFile = open(fileName, "w")
		jsonString = json.dumps(tempAsset.strategy.moneyRecord)
		jsonFile.write(jsonString)
		jsonFile.close()


#################################### COMMAND  #############

if __name__ == "__main__":

	period = 300  ## in sec: This is same as kline interval and also pingtme to exchange for now
	exchange = "alpaca" 
	kline_interval = "5Min"
	moneyPerTrade = 100
	maxNumTrades = 10
	numPreviousCandleStick = 100
	maxPingPerDay = 60
	mockLive = True

	main(period = period, exchange = exchange, kline_interval = kline_interval, moneyPerTrade = moneyPerTrade, \
	    maxNumTrades = maxNumTrades, numPreviousCandleStick = numPreviousCandleStick, maxPingPerDay = maxPingPerDay,\
			 mockLive = mockLive)





			








		