from botindicators import BotIndicators
import numpy as np
from DP import DP_Solver

class NN_optim(object):
	def __init__(self, maxLookBackPrices= 300):

		############# Will only start buying after the max_LookBackPrices reaches the number
		self.predHorizon = 5
		self.pricePred = [0] * self.predHorizon		
		self.dynProgSolver = DP_Solver(self.predHorizon)
		self.maxLookBackPrices = maxLookBackPrices

	def buyOpportunity(self,currentPrice, prices):
		execute_order = 'None'	
		if len(prices)  == self.maxLookBackPrices:
			state = 0  ## Can buy stock
			if (self.portOptimize(state, currentPrice) == 1): ## if portOptimize function call for buying stock
				execute_order = 'Buy'
		return execute_order

	def sellOpportunity(self,currentPrice, prices):
		execute_order = 'None'	
		state = 1  ## Can sell stock
		if len(prices)  == self.maxLookBackPrices:
			if (self.portOptimize(state, currentPrice) == -1): ## if portOptimize function call for sell stock
				execute_order = 'Sell'	
		return execute_order

	def nnPrediction(self, NN_pre, prices):
		temp_prices = np.zeros([1,self.maxLookBackPrices])
		temp_prices[0] = np.asarray(prices)
		temp_pricePred = NN_pre.evaluateNNPrediction(temp_prices)
		temp_pricePred = np.squeeze(temp_pricePred)
		self.pricePred = temp_pricePred.tolist()
		print('pp ', self.pricePred)
		return self.pricePred

	def portOptimize(self, state, currentPrice):
		price_temp = [currentPrice] + self.pricePred
		############################## TC = 0 for now change
		action = self.dynProgSolver.evaluateDP(state, price_temp, 0) 
		# if state == 0:
		# 	action = 1
		return action
