from botindicators import BotIndicators
import numpy as np

class maPriceCrossover(object):
	def __init__(self, shortSMA= 12, longSMA = 26):

		self.indicators = BotIndicators()
		# For maRsiAssist Strategy

		self.shortSMA = shortSMA # number of samples
		self.longSMA = longSMA  # number of samples

	def buyOpportunity(self,currentPrice, prices):
		execute_order = 'None'		
		if (currentPrice < self.indicators.EMA(prices,self.shortSMA)):		
			execute_order = 'Buy'
		return execute_order

	def sellOpportunity(self,currentPrice, prices):
		execute_order = 'None'	
		if (currentPrice > self.indicators.EMA(prices,self.shortSMA)):
			execute_order = 'Sell'	
		return execute_order

