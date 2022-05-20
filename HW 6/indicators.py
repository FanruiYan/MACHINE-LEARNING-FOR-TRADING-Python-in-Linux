"""
Code implementing your indicators as functions that operate on DataFrames.
The “main” method in indicators.py should generate the charts that illustrate your indicators in the report.
"""

"""
Student Name: Fanrui Yan (replace with your name)  		  	   		   	 			  		 			 	 	 		 		 	
GT User ID: fyan40 (replace with your User ID)  		  	   		   	 			  		 			 	 	 		 		 	
GT ID: 903660974 (replace with your GT ID)  	
"""

import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import matplotlib.pyplot as plt
import datetime as dt
from util import get_data


pd.plotting.register_matplotlib_converters()
# Simple Moving Average - SMA
def sma(start_day, end_day, symbol, plot, window_size):

    # get history prices
    history_days = dt.timedelta(window_size * 2)
    history_start_day = start_day - history_days

    # get prices
    df_price = get_data([symbol], pd.date_range(history_start_day, end_day)).ffill().bfill()
    df_price = df_price[[symbol]]

    # calculate SMA
    df_sma = df_price[symbol].rolling(window=window_size).mean()

    # only keep data within the day range
    df_price = df_price.loc[start_day:]
    df_sma = df_sma.loc[start_day:]

    # Normalize
    normalized_df_price = df_price[symbol] / df_price[symbol][0]
    normalized_df_sma = df_sma / df_sma[0]

    # Normalized price/SMA ratio
    p_s = normalized_df_price / normalized_df_sma

    # buy or sell? price/SMA ratio > 1.05 --> sell, price/SMA ratio < 0.95 --> buy

    # Plot
    if plot == True:
        plt.figure(figsize=(10,6))
        plt.title("{} Days EMA".format(window_size))
        plt.xlabel("Date")
        plt.ylabel("Normalized Pirce")
        plt.xticks(rotation=30)
        plt.grid()
        plt.plot(normalized_df_price, label="Normalized Price", color = "#868679")
        plt.plot(normalized_df_sma, label="{} Days SMA".format(window_size), color = "#ffff00")
        plt.plot(p_s, label="Price/SMA ratio", color="red")
        plt.legend()
        plt.savefig("indicator_sma.png")
        #plt.show()
        plt.clf()

    return b_s

# Bollinger Bands
def Bollinger_Bands(start_day, end_day, symbol, plot, window_size):

    # get history prices
    history_days = dt.timedelta(window_size * 2)
    history_start_day = start_day - history_days

    # get prices
    df_price = get_data([symbol], pd.date_range(history_start_day, end_day)).ffill().bfill()
    df_price = df_price[[symbol]]

    # calculate SMA
    df_sma = df_price[symbol].rolling(window=window_size).mean()

    # calculate upper band
    upper = df_sma + (df_price[symbol].rolling(window=window_size).std() * 2)
    # calculate lower band
    lower = df_sma - (df_price[symbol].rolling(window=window_size).std() * 2)

    # only keep data within the day range
    df_price = df_price.loc[start_day:]
    df_sma = df_sma.loc[start_day:]
    upper = upper.loc[start_day:]
    lower = lower.loc[start_day:]

    # Normalize
    normalized_df_price = df_price[symbol] / df_price[symbol][0]
    normalized_df_sma = df_sma / df_sma[0]
    normalized_upper = upper / upper[0]
    normalized_lower = lower / lower[0]

    # BB%
    bbp = (normalized_df_price - normalized_lower) / (normalized_upper - normalized_lower)

    # buy or sell? bbp < 0 --> buy, bbp > 1 --> sell
    #buy_or_sell = normalized_df_sma - normalized_df_price

    # Plot
    if plot == True:
        fig = plt.figure(figsize=(10, 6))
        plt.suptitle("Bollinger Bands ({} Days SMA)".format(window_size))
        plt.xlabel("Date")
        plt.ylabel('Normalized Price')

        ax1 = plt.subplot(211)
        plt.plot(normalized_df_price, label="Normalized Price", color="#868679")
        plt.plot(normalized_df_sma, label="{} Days SMA".format(window_size), color="#ffff00")
        plt.plot(normalized_upper, label="Bollinger Bands", color="#AEBD38")
        plt.plot(normalized_lower, label="Bollinger Bands", color="#AEBD38")
        ax1.legend()
        plt.xlabel("Date")
        plt.ylabel('Normalized price')
        ax1.grid()

        ax2 = plt.subplot(212)
        plt.plot(bbp, label="Bollinger Band %", color="red")
        ax2.grid()
        plt.xlabel("Date")
        ax2.legend()

        fig.autofmt_xdate()
        plt.savefig("indicator_Bollinger Bands.png")
        # plt.show()
        plt.clf()


    return upper, lower

# Momentum
def Momentum(start_day, end_day, symbol, plot, window_size):

    # get history prices
    history_days = dt.timedelta(window_size * 2)
    history_start_day = start_day - history_days

    # get prices
    df_price = get_data([symbol], pd.date_range(history_start_day, end_day)).ffill().bfill()
    df_price = df_price[[symbol]]

    # calculate Momentum
    window_size_days_before_start_day = df_price.loc[:start_day].tail(window_size).index[0]
    list_of_days = df_price.loc[start_day:]
    df_Momentum = list_of_days
    df_Momentum.rename(columns={symbol:"momentum"}, inplace=True)
    list_of_days_minus_window_size = list(df_price.loc[window_size_days_before_start_day:].index)
    i=0
    for day in list_of_days.index:
        #df_Momentum.at[day, 'momentum'] = (df_price.at[day, symbol] / df_price.at[list_of_days_minus_window_size[i], symbol]) - 1
        df_Momentum.at[day, 'momentum'] = df_price.at[day, symbol] - df_price.at[list_of_days_minus_window_size[i], symbol]
        i+=1

    # only keep data within the day range
    df_price = df_price.loc[start_day:]

    # Normalize
    normalized_df_price = df_price[symbol] / df_price[symbol][0]
    normalized_df_momentum = df_Momentum['momentum'] / df_Momentum['momentum'][0]

    # Plot
    if plot == True:
        plt.figure(figsize=(10,6))
        plt.title("{} Days Momentum".format(window_size))
        plt.xlabel("Date")
        plt.ylabel("Pirce")
        plt.xticks(rotation=30)
        plt.grid()
        #plt.plot(df_price[symbol], label="Price", color = "#868679")
        #plt.plot(df_Momentum['momentum'], label="{} Days Momentum".format(window_size), color = "#ffff00")
        plt.plot(normalized_df_price, label="Price", color = "#868679")
        plt.plot(normalized_df_momentum, label="{} Days Momentum".format(window_size), color = "#ffff00")
        plt.legend()
        plt.savefig("indicator_Momentum.png")
        #plt.show()
        plt.clf()

    return df_Momentum


# Exponential Moving Average - EMA
def ema(start_day, end_day, symbol, plot = False, window_size = 20):

    # get history prices to calculate the ema for the first window_size - 1 days
    window_size_x2 = dt.timedelta(window_size * 2)
    history_start_day = start_day - window_size_x2

    # get prices
    df_price = get_data([symbol], pd.date_range(history_start_day, end_day)).ffill().bfill()
    df_price = df_price[[symbol]]

    # calculate EMA
    df_ema = df_price.ewm(span=window_size, adjust=False).mean()

    # only keep data within the day range
    df_price = df_price.loc[start_day:]
    df_ema = df_ema.loc[start_day:]

    # Normalize
    normalized_df_price = df_price[symbol] / df_price[symbol][0]
    normalized_df_ema = df_ema[symbol] / df_ema[symbol][0]

    # buy or sell? positive --> buy, negative --> sell
    buy_or_sell = normalized_df_ema - normalized_df_price

    # Plot
    if plot == True:
        plt.figure(figsize=(10,6))
        plt.title("{} Days EMA".format(window_size))
        plt.xlabel("Date")
        plt.ylabel("Normalized Pirce")
        plt.xticks(rotation=30)
        plt.grid()
        plt.plot(normalized_df_price, label="Normalized Price", color = "#868679")
        plt.plot(normalized_df_ema, label="{} Days EMA".format(window_size), color = "#ffff00")
        plt.legend()
        plt.savefig("indicator_ema.png")
        #plt.show()
        plt.clf()

    return buy_or_sell


# MACD: Moving Average Convergence Divergence
def macd(start_day, end_day, symbol, plot = False):

    # get history prices of 52 days prior to start day
    window_size_x2 = dt.timedelta(52)
    history_start_day = start_day - window_size_x2

    # get prices
    df_price = get_data([symbol], pd.date_range(history_start_day, end_day)).ffill().bfill()
    df_price = df_price[[symbol]].loc[start_day:]

    # calculate EMA for 26 period
    df_ema_26 = df_price.ewm(span=26, adjust=False).mean()
    df_ema_26 = df_ema_26.loc[start_day:]

    # calculate EMA for 12 period
    df_ema_12 = df_price.ewm(span=12, adjust=False).mean()
    df_ema_12 = df_ema_12.loc[start_day:]

    # calculate MACD
    macd = df_ema_12 - df_ema_26

    # calculate EMA for 9 period
    macd_ema_9 = macd.ewm(span=9, adjust=False).mean()
    macd_ema_9 = macd_ema_9.loc[start_day:]

    # normalize
    normalized_df_price = df_price[symbol] / df_price[symbol][0]
    normalized_df_ema_26 = df_ema_26[symbol] / df_ema_26[symbol][0]
    normalized_df_ema_12 = df_ema_12[symbol] / df_ema_12[symbol][0]

    # buy or sell? positive --> buy, negative --> sell
    buy_or_sell = macd - macd_ema_9

    if plot == True:
        fig = plt.figure(figsize=(10,6))
        plt.suptitle("MACD")
        plt.xlabel("Date")
        plt.ylabel('Normalized Price')

        ax1 = plt.subplot(211)
        ax1.plot(normalized_df_ema_12, label="12 Days EMA", color = "#BA5536")
        ax1.plot(normalized_df_ema_26, label="26 Days EMA", color = "#336B87")
        ax1.plot(normalized_df_price, label="Dormalized Price", color = "#505160")
        ax1.legend()
        plt.xlabel("Date")
        plt.ylabel('Normalized price')
        ax1.grid()

        ax2 = plt.subplot(212)
        ax2.plot(macd, label="MACD", color = "#598234")
        ax2.plot(macd_ema_9, label="MACD Signal", color = "#AEBD38")
        ax2.grid()
        plt.xlabel("Date")
        ax2.legend()

        fig.autofmt_xdate()
        plt.savefig("indicator_macd.png")
        #plt.show()
        plt.clf()

    return buy_or_sell


def author():
    return 'fyan40'

if __name__ == "__main__":
	#sma(start_day=dt.datetime(2008, 1, 1), end_day=dt.datetime(2009,12,31), symbol='JPM', plot=False, window_size=20)
    pass