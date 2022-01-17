# Trade with Alpaca/ Binance with stocks/ Crypto
Current version is not working. In a week or two I will update the codes, include setup.py and updated readme. 

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



## SOme Other Notes for reference

Where RSI doesn't work

RSI computes no. of days in up, and no. of days in down. RSI = (up days)/ (up days + down days)  approximately.

1) A slow fall in prices can lead to RSI <20
2) Sharp fall followed by constnat price leads to problems



1) in bot strategy cash updates when there is a profit or a losss. make that correction
2) we can submit stoploss and profit taking when we buy. I don't ae to check it programmatically
3) Plot live OR print for now:  done printing
4) check for mockLive and correct the code if wrong :   DOne

5) Rather than taking the data from alpaca for past 100. We can also take last day data


