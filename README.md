# Trade with Alpaca/ Binance with stocks/ Crypto
Current version works for crypto trading with but need some changes to work with Alpaca. In a week or two I will update the codes, include setup.py and updated readme. 

To follow the codes, Go to live.py. 
You also need to create a free account on alpaca and add the api_key and api_secret_key to botchart.py (line 24 and line 25)		

# Class Details:
All the classes have descriptive names: 
botchart: keep a record of current price (open high low close volume)
botstategy: encodes strategy
bottrade: keep a record of all the trades
botlog: logging
Different Strategieis codes:
maRSI
maRSI Assist
NN_ Dynamic Porgramming



## SOme Other Notes for future reference

Where RSI doesn't work

RSI computes no. of days in up, and no. of days in down. RSI = (up days)/ (up days + down days)  approximately.

1) A slow fall in prices can lead to RSI <20
2) Sharp fall followed by constant price leads to problems
3) Neural Network based Dynamic programming algorithm yields consisitent profits earlier in a good market. Need seperate strategy for the bad market 


Coding Notes (Future release will have)
1) in bot strategy: Add a feature to allow constant or non constant transaction to make portfolio decision.  
2) Submit stoploss and profit taking when we buy on binance (binance just added that). Sometimes due to connection issues price doesn't update, so can't wait for the code to make a decision.
3) Plot live OR print for now:  done printing
4) Update mockLive feature
5) Rather than taking the data from alpaca for past 100. We can also take last day data


