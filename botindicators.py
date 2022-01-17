import numpy as np

class BotIndicators(object):
	def __init__(self):
		 pass
 

	def SMA(self, prices, period):
		if (len(prices) > 0):
			return sum(prices[-period:]) / float(len(prices[-period:]))

	def momentum (self, dataPoints, period=14):
		if (len(dataPoints) > period -1):
			return dataPoints[-1] * 100 / dataPoints[-period]

	def EMA(self, prices, period):
		if (len(prices) > 0):
			x = np.asarray(prices[-period:])
			weights = None
			weights = np.exp(np.linspace(-1., 0., min(period,len(prices))))
			weights /= weights.sum()			
			a = np.dot(x, weights)		
			return a

	def MACD(self, prices, nslow=26, nfast=12):
		emaslow = self.EMA(prices, nslow)
		emafast = self.EMA(prices, nfast)
		return emaslow, emafast, emafast - emaslow

	def slope_divergence(self, prices, period_new = 10, period_old = 30, bounds  = 1):
		slope_new = 0
		slope_old = 0
		slope_n_o_ratio = 0
		if (len(prices) > period_new + period_old):
			slope_new = (prices[-1] - prices[-period_new])/period_new
			slope_old = (prices[-period_new] - prices[-period_old])/period_old
			# if abs(slope_old) <= bounds :
			# 	slope_n_o_ratio = slope_new/bounds
			# else:
			# 	slope_n_o_ratio = slope_new/slope_old
			slope_n_o_ratio = slope_new - slope_old
			
		return slope_new, slope_old, slope_n_o_ratio

	def RSI (self, prices, period=20, method = "SMA"):  ########### Not based on open and close
		rsi = 50
		if (len(prices) > period):
			deltas = np.diff(prices)
			seed = deltas[-period:]

			upData= np.zeros_like(seed)
			upData[seed>=0] = seed[seed>=0]

			downData= np.zeros_like(seed)
			downData[seed<0] = seed[seed<0]
			downData = -1*downData

			if method == "SMA":
				up = upData.sum()/period
				down = downData.sum()/period
			elif method == "EMA":
				up   = self.EMA(upData, period)
				down = self.EMA(downData, period)
			

			# rs = up/down
			rsi = 100*up/ (up+down)		
			# rsi = 100. - 100./(1. + rs)

		return rsi
 
