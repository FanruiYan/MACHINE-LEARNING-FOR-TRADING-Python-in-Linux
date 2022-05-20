"""
Create a set of trades representing the best a strategy could possibly do during the in-sample period using JPM
use $0.00 and 0.0 for commissions and impact
+1000 / -1000 / 0   max trading 2000   shares
"""

"""
Student Name: Fanrui Yan (replace with your name)  		  	   		   	 			  		 			 	 	 		 		 	
GT User ID: fyan40 (replace with your User ID)  		  	   		   	 			  		 			 	 	 		 		 	
GT ID: 903660974 (replace with your GT ID)  	
"""


from util import get_data, plot_data
import datetime as dt
import pandas as pd
from marketsimcode import compute_portvals
import matplotlib.pyplot as plt

def testPolicy(symbol, sd, ed, sv):

	symbol = symbol
	# get stock prices
	df = get_data([symbol], pd.date_range(sd, ed)).ffill().bfill()
	price_df = df[[symbol]]

	# create df to document trade
	df_trades = price_df
	dates = price_df.index

	# keep track of shares of stock currently owned
	share_ownd = 0

	# making trades
		# if next day price higher than today, buy
		# if next day price lower than today, sell/short
		# if next day price equal today, hold
	for i in range(len(dates)-1):
		if price_df.at[dates[i+1], symbol] > price_df.at[dates[i], symbol]:
			df_trades.at[dates[i], symbol] = 1000 - share_ownd
		elif price_df.at[dates[i + 1], symbol] < price_df.at[dates[i], symbol]:
			df_trades.at[dates[i], symbol] = -1000 - share_ownd
		else:
			df_trades.at[dates[i], symbol] = 0
		share_ownd += df_trades.at[dates[i], symbol]
	df_trades.at[dates[len(dates)-1], symbol] = 0

	return df_trades

def author():
	return 'fyan40'

if __name__ == "__main__":
	pass
