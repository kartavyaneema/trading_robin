import time
import urllib.error
import os

from botchart import BotChart
from botstrategy import BotStrategy
from botlog import BotLog
from botcandlestick import BotCandlestick
# from botprediction import BotPrediction
import csv


def main():
	with open('sp500.csv', newline='') as f:
		reader = csv.reader(f)
		data = list(reader)

	data = ['AGNC', 'AMC', 'AMZN', 'CCL', 'CMI', 'CIM', 'DDD', 'EPR', 'MEDS', 'MSFT', 'PFE', 'SAVA', 'TSLA' ]
	data = [ 'TSLA' ]
	for i in data:
		orderSymbol = i[0]
		print(i)
		main_2(orderSymbol)



def main_2(orderSymbol = 'MSFT'):

	mockLive = True
	period = 300 # not needed for binance, 300 sec
	pingTime = period  # Ping time at exchange in seconds
	exchange = "alpaca" ## binance
	orderSymbol = orderSymbol

	if exchange == 'binance':
		kline_interval = "5Min"  # make kline time same as ping interval
	elif exchange =='alpaca':
		kline_interval = '5Min'  ## 5Min, '1D'

	chart = BotChart(exchange =exchange, pair=orderSymbol, period=period, kline_interval=kline_interval, 
		startTime=1516064800, endTime=1516164800, backtest=False)

	strategy = BotStrategy(chart.client, exchange, orderSymbol, backtest=False, mockLive = True)  
	#strategy.testFunction()

	candlesticks = []
	developingCandlestick = BotCandlestick(period) # delete period if not working


	counter = 0
	while counter < 550:
		try:
			if exchange == 'alpaca' or exchange == "binance":
				developingCandlestick = chart.getCandleStick()  # Will directly return a candlestick object: to reduce number of ping
			
			else:
				developingCandlestick.tick(chart.getCurrentPrice())
		except urllib.error.URLError:
			print('error handed this time ')
			time.sleep(int(30))
			if exchange == 'alpaca' or exchange == "binance":
				developingCandlestick = chart.getCandleStick()  # Will directly return a candlestick object: to reduce number of ping
			else:
				developingCandlestick.tick(chart.getCurrentPrice())

		if (developingCandlestick.isClosed()):
			candlesticks.append(developingCandlestick)
			strategy.tick(developingCandlestick)
			developingCandlestick = BotCandlestick(period)
		
		time.sleep(int(pingTime))          ############# 
		counter = counter + 1
	#print("price: ", strategy.prices)

	# Closing logging File
	strategy.outputText.close()
	strategy.moneyRecord.close()
	strategy.tradeRecord.close()

	

	


if __name__ == "__main__":
	main()