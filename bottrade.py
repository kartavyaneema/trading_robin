from botlog import BotLog
from binance.client import Client
# from binance.enums import *

class BotTrade(object):
	def __init__(self,client, currentPrice, exchange,stopLossPercent = 0.5, backtest=True, \
				 tranFeeBuy = 0, tranFeeSell = 0, money_invested = 0., num_stock = 0., orderSymbol='BTCUSDT', mockLive = True, profitTakingPercent = 1):
		self.status = "OPEN"
		self.bidPrice = ""
		self.entryPrice = "" # buy  price 
		self.exitPrice = ""             # sell price
		# print("Trade opened")
		
		# for trading on exchange
		self.exchangeStatus = ""  # buyExecuted, sellWaiting, sellExecuted, cancelWaiting, cancelExecuted: Intially it will be in buyWaiting
		self.orderID = ""   # OderID to query exchange
		self.orderSymbol = orderSymbol # order Symbol to query exhachange (Binance need it)
		self.exchange = exchange
		self.client = client
		self.backtest = backtest
		self.mockLive = mockLive

		self.floating_point_format = 6

		self.tranFeeBuy = tranFeeBuy
		self.tranFeeSell = tranFeeSell
		self.num_stock = round(num_stock, self.floating_point_format)
		self.money_invested = money_invested
		self.stopLossPercent = stopLossPercent
		self.profitTakingPercent = profitTakingPercent
		self.stopLoss = 0
		self.profitTaking = 0

		# for adjusting cash value in botstrategy for live trading
		''' self.adjusted_cost: flag that says if the the true money invested is adjusted with 
		initial order
		self.adjusted_cost_val is the value of tjhe cost adjsted: Money_invested_bid - money_invested_true
		'''
		self.adjusted_cost = 0 
		self.adjusted_cost_val = 0


	def buy(self, currentPrice, timeCandle):

		if self.backtest or self.mockLive:			 
			self.orderID = 1111 ## Not needed 
			self.exchangeStatus = "buyExecuted"			
			self.entryPrice = currentPrice*(1+self.tranFeeBuy)
			self.bidPrice   = currentPrice*(1+self.tranFeeBuy)
			self.num_stock = round(self.money_invested/currentPrice, self.floating_point_format)
			self.stopLoss = self.entryPrice*(1- self.stopLossPercent/100)	 ################ Changing stopLoss as the priceto sell below
			self.profitTaking = self.entryPrice*(1+ self.profitTakingPercent/100)	 ################ Changing stopLoss as the priceto sell below
			
			print("Time ", timeCandle, ', ', self.orderSymbol, " buy order is executed at ", self.entryPrice)

		else: 
			if self.exchange == "binance":
				# Below 2 lines are added because binance api has an error (refer version control document)
				recent_trade_temp = self.client.get_recent_trades(symbol=self.orderSymbol,limit=1)
				self.entryPrice = float(recent_trade_temp[0]['price'])

				tempResult = self.client.create_order(symbol=self.orderSymbol, side='BUY', \
							 type='MARKET', quantity=self.num_stock)				 
				self.orderID = tempResult['orderId']
				self.exchangeStatus = "buyWaiting"
				print("On exchange: buy order is placed")	
				self.bidPrice   = currentPrice*(1+self.tranFeeBuy)

	
	def cancelBuy(self): # Backtest doesn't check this function for now
		if self.exchangeStatus == "buyWaiting":
			if self.exchange == "binance":
				tempResult = self.client.cancel_order(symbol=self.orderSymbol,orderId=self.orderID)  # This can give multiple cancel orders if there is a network problem: It may give an error in binance
				self.exchangeStatus = "cancelWaiting" # this is handling the case when we cancel the order however it didn't pass due to network problem
				self.status = "OPEN"
				print("Buy order is given cancel order")

	def sell(self,currentPrice,timeCandle):
		if self.backtest or self.mockLive:
			self.exchangeStatus = "sellWaiting"			
			self.exitPrice = currentPrice*(1-self.tranFeeSell)
			self.money_invested = self.num_stock*self.exitPrice # money return after selling
			# self.close()
			print("Time ", timeCandle, ', ', self.orderSymbol, " sell order is executed at ", self.exitPrice)


		else:
			if self.exchangeStatus == "buyExecuted":
				if self.exchange == "binance":
					# Below 2 lines are added because binance api has an error (refer version control document)
					recent_trade_temp = self.client.get_recent_trades(symbol=self.orderSymbol,limit=1)
					self.exitPrice = float(recent_trade_temp[0]['price'])
					print('num_stock ', self.num_stock)
					print('exitPrice ', self.exitPrice)
					'''
					we can not sell the same num. of stock we bought, as binance takes a transaction cost of .1%. 
					SO our num_stock reduced by (1-fee)*num_stock. In the logic, I just changed the 
					submitted num stock. However not changing quan in self.num_stock. 
					As total money recieved after tracnsaction is complete will be same as:
					 (1-fee)price*num stock = price*(1-fee)num stock '''
					stock_order_quan = round(self.num_stock*(1-self.tranFeeSell),self.floating_point_format)
					tempResult = self.client.create_order(symbol=self.orderSymbol, side='SELL', \
							     type='MARKET', quantity=stock_order_quan) 
					self.orderID = tempResult['orderId'] ############### sell order ID
					self.exchangeStatus = "sellWaiting"
					print("On Exchange: Sell order is placed")
					# self.exitPrice = currentPrice

	def close(self):
		self.status = "CLOSED"		
		print("Trade closed")

	def profit(self,sell):
		profit = (self.exitPrice - self.entryPrice)*self.num_stock

	def tick(self, currentPrice, timeCandle):   ########### Change this for stoploss	
		sellDueTo_StopLoss_ProfitTaking = False

		if (currentPrice < self.stopLoss):
			print("stoploss Hit")
			sellDueTo_StopLoss_ProfitTaking = True

		elif (currentPrice > self.profitTaking):			
			print("profitTaking Hit")
			sellDueTo_StopLoss_ProfitTaking = True

		return sellDueTo_StopLoss_ProfitTaking


	def showTrade(self):  # Just for displaying, don't worry
		tradeStatus = "Entry Price: "+str(self.entryPrice)+" Status: "+str(self.status)+" Exit Price: "+str(self.exitPrice)

		if ((self.status == "CLOSED") and (self.exchangeStatus == "sellExecuted")):  ## This code turns the log to green if trade is profitable other red. Dont' worry
			tradeStatus = tradeStatus + " Profit: "
			if (self.exitPrice > self.entryPrice):
				tradeStatus = tradeStatus + "\033[92m"
			else:
				tradeStatus = tradeStatus + "\033[91m"

			tradeStatus = tradeStatus+str(self.exitPrice - self.entryPrice)+"\033[0m"

		print(tradeStatus)

	def checkStatusExchange(self, timeCandle):  # Check status on exchange if the order is executed
		if self.backtest or self.mockLive:
			if self.exchangeStatus == "sellWaiting":
				self.exchangeStatus = "sellExecuted"
				# Write a function for profit
				self.close()
		else:

			tempStatusOld = self.exchangeStatus

			if self.exchange == "binance":
				tempStatus = self.client.get_order(symbol=self.orderSymbol,orderId=self.orderID)  ## change client later
				if tempStatus['status'] == 'NEW':
					self.exchangeStatus = tempStatusOld  # Don't do anything

				elif tempStatus['status'] == 'CANCELED':  # Order has beed succesfully canceled: close trade.status
					self.exchangeStatus = "cancelExecuted"
					self.close()  # this is handling the case when we cancel the order however it didn't pass due to network problem

				elif tempStatus['status'] == 'FILLED':
					if ((tempStatusOld == "buyWaiting") or  (tempStatusOld == "cancelWaiting")):
						self.exchangeStatus = "buyExecuted"	

						# self.entryPrice = float(tempStatus['price'])*(1+self.tranFeeBuy)
						self.entryPrice = self.entryPrice*(1+self.tranFeeBuy)
						self.num_stock = float(tempStatus['executedQty'])

						'''calculating money_invested again as bid price can be different from
							entryPrice. Also calcuate the difference in the bided money invested and true
							money invested
						'''	
						money_invested_true = 	self.entryPrice*self.num_stock  	
						self.adjusted_cost_val = self.money_invested - money_invested_true
						self.money_invested = money_invested_true
						self.stopLoss = self.entryPrice*(1- self.stopLossPercent/100)	 ################ Changing stopLoss as the priceto sell below
						print('money invest true ', money_invested_true)
						print('adjusted_cost_val ', self.adjusted_cost_val)


					if tempStatusOld == "sellWaiting":
						self.exchangeStatus = "sellExecuted"
						# self.exitPrice = float(tempStatus['price'])	*(1-self.tranFeeSell)
						self.exitPrice = self.exitPrice*(1-self.tranFeeSell)
						# self.money_invested = float(tempStatus['executedQty'])*float(tempStatus['price']) # total money obtained at selling
						self.money_invested = float(tempStatus['executedQty'])*self.exitPrice # total money obtained at selling
					
						# Write a function for profit
						self.close()







	