import numpy as np

class BotStrategy(object):
	def __init__(self, client, exchange, orderSymbol, backtest=True):
		self.output = BotLog("trial.txt")
		self.prices = []