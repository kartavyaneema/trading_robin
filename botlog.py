class BotLog(object):
	def __init__(self, filename):
		self.outputText = open(filename,'a')	# Apend to file	
		

	def log(self, message):
		print(message)

	def writeData(self, timeCandle, price, action, num_stock):		
		self.outputText.write(str(timeCandle) +","+ str(price)+","+ str(action) \
			 +","+ str(num_stock))
		self.outputText.write("\n")
