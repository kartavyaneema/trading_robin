from botlog import BotLog
from botindicators import BotIndicators
from bottrade import BotTrade
from binance.client import Client

from maRSI import maRSI
from maPriceCrossover import maPriceCrossover
import json

import time
import datetime as dt
import numpy as np

class BotStrategy(object):
	def __init__(self, client, exchange = 'alpaca', orderSymbol = 'MSFT', backtest=False, mockLive = False, equity_money = 0, cash = 100):
		self.stockPriceRecord  = []
		self.moneyRecord = [] # open("./Data/"+ orderSymbol + "_moneyRecord.txt",'w')  # total_money, equity_money, cash
		self.tradeRecord  =[] # open("./Data/"+ orderSymbol + "_tradeRecord.txt",'w')
		self.prices = []
		self.lowP = []
		self.highP = []
		self.volatility = [] ## Average volatility of past some days
		self.SMA_fast_history = []
		self.SMA_slow_history = []
		self.avg_volatility = .5 ### percent
		self.closes = [] # Needed for Momentum Indicator
		self.trades = []
		self.currentPrice = ""
		self.currentClose = ""
		self.numSimulTrades = 1		
		self.orderSymbol = orderSymbol # order Symbol to query exhachange (Binance need it)
		self.exchange = exchange
		self.client = client
		self.backtest = backtest
		self.mockLive = mockLive			
		self.equity_money = equity_money
		self.cash = cash
		self.total_money_init = cash
		self.total_money = cash
		#self.orderStatus = 'NULL' # Buy, Sell : This variable is defined for logging

		self.indicators = BotIndicators()

		########### For Strategy
		self.strategySel = "maRSI" # "maRSI", NN_optim, maPriceCrossover
		self.maxLookBackPrices = 300  # should be greater than minimu number required for all the strategies

		self.ma_rsi = maRSI()
		self.ma_pc = maPriceCrossover()  ## maPriceCrossover

		## Only for data loging
		self.shortSMA = 10 # number of samples
		self.longSMA = 20  # number of samples

	def tick(self,candlestick, evaluateTradingOptions = True, evaluateOnlySell = False):
		
		self.currentPrice = float(candlestick.close)  ## Putting Close price here
		self.prices.append(self.currentPrice)
		self.lowP.append(float(candlestick.low))
		self.highP.append(float(candlestick.high))
		self.volatility.append(candlestick.volatility)
		if len(self.prices) >self.maxLookBackPrices: # Maintain the maximum length to maxLookBack
			self.prices.pop(0)
			self.volatility.pop(0)
			self.lowP.pop(0)
			self.highP.pop(0)

		self.dataLog(candlestick) # for logging data

		if evaluateTradingOptions:
			#dt.datetime.fromtimestamp(int(candlestick.startTime)).strftime('%Y-%m-%d %H:%M:%S')
			timeCandle = int(candlestick.startTime) 
			openTrades = []
			openTradesIndex = []				
			openTrades, openTradesIndex = self.keepMoneyRecord(candlestick, timeCandle)  # Main strategy

			## Opening a trade if the number of trades is less than numSimulTrades: buy
			if (evaluateOnlySell == False) and (len(openTrades) < self.numSimulTrades): 
				self.evaluateBuyPositions(openTrades, openTradesIndex, timeCandle)

			self.evaluateSellPositions(openTrades, openTradesIndex, timeCandle)
			self.updateOpenTrades(candlestick)   # for stoploss prevention
			# self.showPositions() # Not needed only for displaying


	def keepMoneyRecord(self, candlestick, timeCandle):		
		openTrades = []
		openTradesIndex = [] # index of trades that are in openTrades
		equity_money_temp = 0.
		counter_temp = 0	
		for trade in self.trades:  ## Extract all the open trades
			if (trade.status == "OPEN"):
				openTrades.append(trade)
				openTradesIndex.append(counter_temp)
				equity_money_temp = equity_money_temp + self.currentPrice*trade.num_stock #money now in stck
			counter_temp = counter_temp + 1

		self.equity_money = equity_money_temp
		self.total_money = self.equity_money + self.cash

		tempDict = {}
		tempDict['timeCandle'] = timeCandle
		tempDict['total_money'] =self.total_money
		tempDict['equity_money'] =self.equity_money
		tempDict['cash'] =self.cash
		self.moneyRecord.append(tempDict)
	
		return openTrades, openTradesIndex		

	def evaluateBuyPositions(self, openTrades, openTradesIndex, timeCandle):
		############### Looking for buying oportunity		 
		#print("\033[43m" + 'stop here ')
		money_invested_temp = self.cash ## only 90% money we will ask to invest
		if self.strategySel == "maPriceCrossover":
			## Strategy 1: MA-price crossover strategy
			if self.ma_pc.buyOpportunity(self.currentPrice, self.prices) == 'Buy':					
				self.buyStock(money_invested_temp, timeCandle)

		elif self.strategySel == "maRSI":
			if self.ma_rsi.buyOpportunity(self.currentPrice, self.prices) == 'Buy':
				self.buyStock(money_invested_temp, timeCandle)


	def evaluateSellPositions(self, openTrades, openTradesIndex, timeCandle):
		############### Looking for Selling or canceling order oportunity					
		counter_temp = -1
		for trade in openTrades:  ## Deciding to close the open trades: sell or cancel trade
			counter_temp = counter_temp+1
			trade.checkStatusExchange(timeCandle)
			
			if trade.exchangeStatus == "buyWaiting":   # CancelBuyOrder# Update with buy executed type logic

				if self.strategySel == "maPriceCrossover":
					if self.ma_pc.sellOpportunity(self.currentPrice, self.prices) == 'Sell':
						trade.cancelBuy()################ Update this with maRSI strategy

				elif self.strategySel == "maRSI":
				## Strategy 2: MA Bull Hammer (Swing, trend)
					if self.ma_rsi.sellOpportunity(self.currentPrice, self.prices) == 'Sell':
						trade.cancelBuy()



			elif trade.exchangeStatus == "buyExecuted": # sell buy order

				if trade.adjusted_cost == 0:  ## adjust the available cash with the true cost executed
					self.cash = self.cash + trade.adjusted_cost_val
					trade.adjusted_cost = 1
					# Writing to file that trade has been executed			
					
					tempDict = {}
					tempDict['timeCandle'] = timeCandle					
					tempDict['entryPrice'] = trade.entryPrice
					tempDict['Transaction'] = 'Buy'
					tempDict['num_stock'] = trade.num_stock

					self.tradeRecord.append(tempDict)



				## Check the Stop Loss and Profit Taking
				sellDueTo_StopLoss_ProfitTaking = trade.tick(self.currentPrice, timeCandle)

				if self.strategySel == "maPriceCrossover":
					if self.ma_pc.sellOpportunity(self.currentPrice, self.prices) == 'Sell' or sellDueTo_StopLoss_ProfitTaking:
						trade.sell(self.currentPrice, timeCandle)

				elif self.strategySel == "maRSI":
				## Strategy 2: MA Bull Hammer (Swing, trend)
					if self.ma_rsi.sellOpportunity(self.currentPrice, self.prices) == 'Sell':
						pass
						# trade.sell(self.currentPrice, timeCandle)
					if sellDueTo_StopLoss_ProfitTaking:
						trade.sell(self.currentPrice, timeCandle)



			elif trade.exchangeStatus == "cancelExecuted":
				self.cash = self.cash + trade.money_invested
				indexToRemoveTrades = openTradesIndex[counter_temp]
				del self.trades[indexToRemoveTrades]

			elif trade.exchangeStatus == "sellExecuted":
				# We changed money_invested to money_obtained after selling is executed
				self.cash = self.cash + trade.money_invested
								
				tempDict = {}
				tempDict['timeCandle'] = timeCandle					
				tempDict['exitPrice'] = trade.exitPrice
				tempDict['Transaction'] = 'Sell'
				tempDict['num_stock'] = trade.num_stock
				self.tradeRecord.append(tempDict)

				indexToRemoveTrades = openTradesIndex[counter_temp]
				del self.trades[indexToRemoveTrades] 

				# "Nothing Needed as trade.status will be close"


	def updateOpenTrades(self, candlestick):  # Sell in case of stoploss
		timeCandle = int(candlestick.startTime)
		for trade in self.trades:  ## Note trade is the object of BotTrade (**)
			if ((trade.status == "OPEN") and (trade.exchangeStatus == "buyExecuted")):
				trade.tick(self.currentPrice, timeCandle)

	def showPositions(self):
		for trade in self.trades:
			trade.showTrade()

	def testFunction(self):
		print(self.client.get_asset_balance(asset='ETH') )# get balance

	def dataLog(self, candlestick):		
		tempDict = {}
		tempDict['timeCandle'] =  int(candlestick.startTime)
		tempDict['open'] = candlestick.open
		tempDict['high'] = candlestick.high
		tempDict['low'] = candlestick.low
		tempDict['close'] = candlestick.close		
		tempDict['volume'] = candlestick.volume
		tempDict['priceAverage'] = candlestick.priceAverage
		tempDict['SMA_' + str(int(self.shortSMA))] = self.indicators.SMA(self.prices,self.shortSMA)
		tempDict['SMA_' + str(int(self.longSMA))] = self.indicators.SMA(self.prices,self.longSMA)
		tempDict['RSI'] = self.indicators.RSI(self.prices)

		self.stockPriceRecord.append(tempDict)



	def buyStock(self, money_invested_temp, timeCandle):
		self.cash = self.cash - money_invested_temp
		tempBotTrade = BotTrade(self.client, self.currentPrice, self.exchange, \
			backtest=self.backtest, money_invested = money_invested_temp, \
			num_stock = money_invested_temp/self.currentPrice,orderSymbol=self.orderSymbol, mockLive = self.mockLive) 				
		tempBotTrade.buy(self.currentPrice, timeCandle) # for live trd add code for actual bought price
		self.trades.append(tempBotTrade)  ## ** BotTrade







