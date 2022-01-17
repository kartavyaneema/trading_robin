import sys, getopt
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import datetime as dt
from random import *
import matplotlib.animation as animation
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import matplotlib.dates as mdates


# Plotting CandleStick and moving average
pullData = open("moneyRecord.txt","r").read()
dataArray = pullData.split('\n')
timeData = []
moneyTotal  = []
cash  = []
moneyEquity  = []


counter = 0 
for eachLine in dataArray:
	if len(eachLine)>1:
		t,mT, mE, c = eachLine.split(',')
		timeData.append(dt.datetime.fromtimestamp(int(t)))
		moneyTotal.append(float(mT))
		moneyEquity.append(float(mE))
		cash.append(float(c))
		counter = counter + 1
		if counter == 2:
			print('x ' ,mT)


		
# Ploting
print(len(timeData[1:]))

fig = plt.figure()
# ax1 = plt.subplot(211)
# dates = matplotlib.dates.date2num(timeData)
plt.plot(timeData,moneyTotal, label='moneyTotal', linewidth=1 )
# plt.plot(timeData,moneyEquity, label='moneyEquity', linewidth=1) #marker = '+')
# plt.plot(timeData,cash, label='cash', linewidth=1) #  marker = 'o'

plt.legend(loc='upper right')

plt.xticks(rotation='vertical')
plt.gcf().autofmt_xdate()


# max_xticks = 20
# xloc = plt.MaxNLocator(max_xticks)
# ax.xaxis.set_major_locator(xloc)

# plt.locator_params(nbins=10)
# ax.locator_params(nbins=10, axis='x')

# Ploting Buy and sell events
plt.show()

