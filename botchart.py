from poloniex import poloniex
from binance.client import Client
import alpaca_trade_api as tradeapi
import urllib, json
from botcandlestick import BotCandlestick

class BotChart(object):
	def __init__(self, exchange ='alpaca', pair='MSFT', period=60, kline_interval='1Min', startTime=1516064800, endTime=1516164800, backtest=False, numBins = 1000):   # Constructer
		self.pair = pair
		self.period = period
		self.startTime = startTime # 1516064800000
		self.endTime =   endTime # 1516164800000  #1516080000000
		self.kline_interval = kline_interval  # binance require this format
		self.exchange = exchange
		self.backtest = backtest
		self.data = []

		if (self.exchange == "binance"):
			# Intialize the client
			api_key = '' # Please write your key
			api_secret = '' # Please write your key
			self.client = Client(api_key, api_secret)

		elif(self.exchange == "alpaca"):# Intialize the client
			api_key = '<api_key>' # Please write your key
			api_secret = '<api_secret_ley>' # Please write your key
			api_url = 'https://paper-api.alpaca.markets'			
			self.client = tradeapi.REST(api_key, api_secret, api_url)

		if self.backtest and self.exchange == "binance":
			# Get candlestick historical data
			BinData = self.client.get_klines(symbol=self.pair, interval=self.kline_interval, startTime=self.startTime, endTime=self.endTime)
			# print("tum ", BinData[-1])
			while BinData: #int(BinData[-1][6]) < self.endTime:
				# print("all ", type(self.startTime))
				for datum in BinData:
					PriceWeightedAverage = (float(datum[2])+ float(datum[3]) + float(datum[4]))/3.0
					self.data.append(BotCandlestick(self.period,float(datum[1]),float(datum[2]),float(datum[3]),float(datum[4]),PriceWeightedAverage, float(datum[5]), startTime = int(datum[0])/1000 ))
					# [time, open, high, low, close, volume, closeTime, assetVolume, trades, buyBaseVolume, buyAssetVolume, ignored]
				BinData = self.client.get_klines(symbol=self.pair, interval=self.kline_interval, startTime=int(BinData[-1][6]), endTime=self.endTime)
				# print("cross ", BinData[-1][6])


		if self.backtest and self.exchange == "alpaca":
			BinData = self.client.get_barset(self.pair, self.kline_interval, limit=numBins)	
			# print(self.pair)		
			for datum in BinData[self.pair]:
				# print(datum)
				PriceWeightedAverage = (datum.h+ datum.l + datum.c)/3.0
				candlestick_obj = BotCandlestick(period = self.period, open = datum.o, high = datum.h, low = datum.l, \
					close = datum.c, priceAverage = PriceWeightedAverage, volume = datum.v, startTime = int(datum.t.timestamp()))
				
				self.data.append(candlestick_obj)
	
	def getPoints(self):
		return self.data

	def getCurrentPrice(self):
		if (self.exchange == "binance"):
			# Helper function for extracting specific price from Binance
			# It may or may not contain the name price pair asked then add an exception code later
			all_prices = self.client.get_all_tickers()
			index_pair = -1
			for i in range(len(all_prices)):
			    if all_prices[i]['symbol'] == self.pair:
			        index_pair = i
			        break

			lastPairPrice = float(all_prices[index_pair]['price'])
			if (index_pair == -1):
				print("Pair not found in Binance all ticks")
				exit(1)
		return lastPairPrice

	def getCandleStick(self):
		if (self.exchange == "binance"):
			datum = self.client.get_klines(symbol=self.pair, interval=self.kline_interval, limit = 1)
			datum = datum[0]
			print("datum ", datum)
			PriceWeightedAverage = (float(datum[2])+ float(datum[3]) + float(datum[4]))/3.0
			candlestick_obj = BotCandlestick(period = self.period, open = float(datum[1]), high = float(datum[2]), low = float(datum[3]),
				close = float(datum[4]),priceAverage = PriceWeightedAverage, volume = float(datum[5]), startTime = int(datum[0])/1000)
		
		elif (self.exchange == "alpaca"):			
			datum = self.client.get_barset(self.pair, self.kline_interval, limit=2)
			datum = datum[self.pair][1]
			PriceWeightedAverage = (datum.h+ datum.l + datum.c)/3.0
			candlestick_obj = BotCandlestick(period = self.period, open = datum.o, high = datum.h, low = datum.l, \
				close = datum.c, priceAverage = PriceWeightedAverage, volume = datum.v, startTime = int(datum.t.timestamp()))		

		return candlestick_obj


	def getPreviousCandleStick(self, numPreviousCandleStick = 100):
		data = []
		if self.exchange == "alpaca":
			BinData = self.client.get_barset(self.pair, self.kline_interval, limit=numPreviousCandleStick)	
			# print('pair ', self.pair)
			# print('BinData ', BinData)		
			for datum in BinData[self.pair]:
				print(datum)
				PriceWeightedAverage = (datum.h+ datum.l + datum.c)/3.0
				candlestick_obj = BotCandlestick(period = self.period, open = datum.o, high = datum.h, low = datum.l, \
					close = datum.c, priceAverage = PriceWeightedAverage, volume = datum.v, startTime = int(datum.t.timestamp()))
				
				data.append(candlestick_obj)

		return data

	

