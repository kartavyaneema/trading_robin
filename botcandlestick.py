import sys, getopt
import time


class BotCandlestick(object):
	def __init__(self, period=300,open=None,high=None,low=None,close=None,priceAverage=None, volume = None, startTime = time.time()):
		self.current = None
		self.open = open
		self.close = close
		self.high = high
		self.low = low
		self.startTime = startTime		
		self.period = period		
		self.priceAverage = priceAverage
		self.volume = volume
		self.volatility = self.calculateVolatility()

	def tick(self,price):
		self.current = float(price)
		if (self.open is None):
			self.open = self.current

		if ( (self.high is None) or (self.current > self.high) ):
			self.high = self.current

		if ( (self.low is None) or (self.current < self.low) ):
			self.low = self.current

		if ( time.time() >= ( self.startTime + self.period) ):
			self.close = self.current
			self.priceAverage = ( self.high + self.low + self.close ) / float(3)

		print("Open: "+str(self.open)+" Close: "+str(self.close)+" High: "+str(self.high)+" Low: "+str(self.low)+" Current: "+str(self.current))
	
	def calculateVolatility(self):
		return (self.high-self.low)/(self.high+self.low)*100

	def isClosed(self):
		if (self.close is not None):
			return True
		else:
			return False

