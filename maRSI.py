from botindicators import BotIndicators
import numpy as np

class maRSI(object):
	def __init__(self, SMA=26, RsiOverSoldTh = 20, RsiOverBoughtTh = 80):

		# self.maxLookBackPrices = 300  # should be greater than moving average
		# self.shortSMA = 12  # number of samples
		self.SMA = SMA  # number of samples
		self.indicators = BotIndicators()
		# For maRsiAssist Strategy
		self.buyCondition = False
		self.sellCondition = False
		self.RsiOverSoldTh = RsiOverSoldTh
		self.RsiOverBoughtTh = RsiOverBoughtTh
		self.rsi_period = 20

	def buyOpportunity(self,currentPrice, prices):
		execute_order = 'None'
		## Strategy 2: MA Bull Hammer (Swing, trend)
		# if (currentPrice < self.indicators.SMA(prices,self.SMA)):
		if ( self.indicators.RSI(prices, period=self.rsi_period) < self.RsiOverSoldTh):
			self.buyCondition = True
		else:
			check1 = (self.indicators.SMA(prices,10)> self.indicators.SMA(prices,20))
			# if len(prices)>5:
			# 	check2 = (prices[-1] - prices[-2] > 0) and (prices[-2] -  prices[-3] > 0)  # and (prices[-3] -  prices[-4] > 0) 
			# 	check3 = (prices[-1] - prices[-2] > prices[-2] -  prices[-3] ) and (prices[-2] -  prices[-3] > 0)  # and (prices[-3] -  prices[-4] > 0) 
				
			# else:
			# 	check2 = False
			# 	check3 = False
			check2 = (self.indicators.SMA(prices,5)> self.indicators.SMA(prices,10))
			# check3 = (self.indicators.SMA(prices,5)- self.indicators.SMA(prices,10)) > (self.indicators.SMA(prices,10)- self.indicators.SMA(prices,20))

			if self.buyCondition == True and check1: # and check2 :
				if check2:
					execute_order = 'Buy'
				self.buyCondition = False
		# else:
		# 	self.buyCondition = False
		return execute_order

	def sellOpportunity(self,currentPrice, prices):
		execute_order = 'None'	
	## Strategy 2: MA Bull Hammer (Swing, trend)
		if (currentPrice > self.indicators.SMA(prices,self.SMA)):
			if (self.indicators.RSI(prices, period=self.rsi_period) > self.RsiOverBoughtTh):
				self.sellCondition = True
			else:
				if self.sellCondition == True:
					execute_order = 'Sell'					
					self.sellCondition == False
		else:
			self.sellCondition = False
		return execute_order

