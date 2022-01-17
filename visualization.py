import sys, getopt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from random import *
import matplotlib.animation as animation
import matplotlib.ticker as mticker
# from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates
import pandas as pd
import json

def main(orderSymbol, folderName):

	# Plotting CandleStick and moving average
	
	pullData= open(folderName+ orderSymbol + "_stockPriceRecord.json")
	dataArray = json.load(pullData)

	timeData = [dt.datetime.fromtimestamp(i["timeCandle"]) for i in dataArray]
	openP   = [i["open"] for i in dataArray]
	closeP   = [i["close"] for i in dataArray]
	highP  = [i["high"] for i in dataArray]
	lowP  = [i["low"] for i in dataArray]
	Price = [i["priceAverage"] for i in dataArray]
	volume = [i["volume"] for i in dataArray]
	shortSMA = [i["SMA_10"] for i in dataArray]
	longSMA = [i["SMA_20"] for i in dataArray]
	RSI = [i["RSI"] for i in dataArray]


	# Creating data for candle stick
	counter = 0
	lenP = len(openP)
	ohlc = []
	while counter < lenP:
		append_me = timeData[counter], openP[counter], highP[counter], lowP[counter], closeP[counter], volume[counter]
		ohlc.append(append_me)
		counter+=1

	# Extracting data from differnt file
	pullData= open(folderName+ orderSymbol + "_tradeRecord.json")
	dataArray = json.load(pullData)


	timeDataTrades = [dt.datetime.fromtimestamp(i["timeCandle"]) for i in dataArray]	
	priceTrades = [i["entryPrice"] for i in dataArray]
	events = ["green" if i[ "Transaction"] =="Buy" else "red" for i in dataArray ]
					



	######################################## Figure

	index_timeDataTrades = [(timeData.index(i)-1) for i in timeDataTrades]
	timeData = range(len(Price))
	timeDataTrades  = index_timeDataTrades

	fig = plt.figure()
	ax1 = plt.subplot(211)
	plt.plot(timeData,closeP, label='price', linewidth=1) #, marker = '+' )
	plt.plot(timeData,shortSMA, label='shortSMA', linewidth=1) #marker = '+')
	plt.plot(timeData,longSMA, label='longSMA', linewidth=1) #  marker = 'o'
	plt.scatter(timeDataTrades, priceTrades, color=events, label = 'BuySell', s=35)
	plt.legend(loc='upper right')


	## ax2
	ax2 = plt.subplot(212, sharex=ax1)
	# plt.plot(timeData,volume, label='RSI',  marker = '+')
	# plt.plot(timeData,[Price[i]*volume[i] for i in range(len(volume))] )
	plt.plot(timeData,RSI, label='RSI',  marker = '+')
	plt.axhline(y=80, color='r', linestyle='-')
	plt.axhline(y=20, color='r', linestyle='-')
	plt.xticks(rotation='vertical')
	plt.gcf().autofmt_xdate()
	plt.legend(loc='upper right')
	plt.title(orderSymbol)
	plt.show()

	### Call CandleStick
	# candlestickPlot(openP, highP, lowP, closeP)

##############################################################
################ CandleStick Plot
##########################################################
def candlestickPlot(open, high, low, close ):
	dict = {'Open': open, 'High': high, 'Low': low, 'Close': close} 
    
	df = pd.DataFrame(dict)	
	df = df[['Open', 'High', 'Low', 'Close']]
	print(df.head())

	fig, ax1 = plt.subplots(figsize=(14,7), num='figure name')

	ax1.set_title('box title')
	ax1.yaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
	ax1.xaxis.grid(True, linestyle='-', which='major', color='lightgrey', alpha=0.5)
	print(df.index.astype(str))
	bp = ax1.boxplot(df, patch_artist=True, labels=df.index.astype(str))

	# green up, red down
	for count_box in range(len(df.index)):
		if (df.iloc[count_box,0]-df.iloc[count_box,3])>=0:
			plt.setp(bp['boxes'][count_box], color='red')
		else:
			plt.setp(bp['boxes'][count_box], color='green')

	plt.xticks(rotation=30)
	plt.show() #or plt.savefig()


if __name__ == "__main__":

	# folderName = "./Data/RSI20_SF_1020/"
	# data = ['AGNC', 'AMC', 'AMZN', 'CCL', 'CMI', 'CIM', 'DDD', 'EPR', 'MEDS', 'MSFT', 'PFE', 'SAVA', 'TSLA' ]

	folderName = "./Data/sp500/"
	data = ['TYL', 'PAYC', 'MKTX', 'HOLX', 'AES', 'CTXS', 'NRG', 'DISCA'   ]

	folderName = "./Data/sp500_ma5/"
	data = ['XOM', 'BA', 'COP', 'EOG', 'INCY', 'XRAY', 'MRO', 'IVZ' ] ## Loss
	data = ['KLAC', 'RHI', 'WRB', 'WYNN', 'CPW', 'EXPE'] # PROFIT

	folderName = "./Data/19_07_2021/"
	data = [['MSFT'], ['TSLA'], ['FB'], ['PLUG'], ['AMZN'], \
			['GOOG'], ['NVDA'], ['V'], ['DIS'], ['CSCO'], \
			['BA'], ['TJX'], ['CCI'], ['CMG'], ['ZBRA'], \
			['VIAC'], ['GRMN'], ['HOLX'], ['MRO'], ['JNPR'],\
			['FOX'], ['DISCA'], ['UAA'], ['NOV'], ['LEG']]

	data = ['FOX', 'CMG', 'V']

	# folderName = "./Data/"
	# data = ['RCL']
	
	for i in data:
		orderSymbol = i
		print(i)
		main(orderSymbol, folderName)
