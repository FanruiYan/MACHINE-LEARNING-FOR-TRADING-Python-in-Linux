""""""  		  	   		   	 			  		 			 	 	 		 		 	
"""MC2-P1: Market simulator.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		   	 			  		 			 	 	 		 		 	
Atlanta, Georgia 30332  		  	   		   	 			  		 			 	 	 		 		 	
All Rights Reserved  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Template code for CS 4646/7646  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		   	 			  		 			 	 	 		 		 	
works, including solutions to the projects assigned in this course. Students  		  	   		   	 			  		 			 	 	 		 		 	
and other users of this template code are advised not to share it with others  		  	   		   	 			  		 			 	 	 		 		 	
or to make it available on publicly viewable websites including repositories  		  	   		   	 			  		 			 	 	 		 		 	
such as github and gitlab.  This copyright statement should not be removed  		  	   		   	 			  		 			 	 	 		 		 	
or edited.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
We do grant permission to share solutions privately with non-students such  		  	   		   	 			  		 			 	 	 		 		 	
as potential employers. However, sharing with other current or future  		  	   		   	 			  		 			 	 	 		 		 	
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		   	 			  		 			 	 	 		 		 	
GT honor code violation.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
-----do not edit anything above this line---  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
Student Name: Fanrui Yan (replace with your name)  		  	   		   	 			  		 			 	 	 		 		 	
GT User ID: fyan40 (replace with your User ID)  		  	   		   	 			  		 			 	 	 		 		 	
GT ID: 903660974 (replace with your GT ID)  		  	   		   	 			  		 			 	 	 		 		 	
"""  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
import datetime as dt  		  	   		   	 			  		 			 	 	 		 		 	
import os  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
import numpy as np  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
import pandas as pd  		  	   		   	 			  		 			 	 	 		 		 	
from util import get_data, plot_data  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
pd.set_option('float_format', '{:f}'.format)
def compute_portvals(orders_file="./orders/orders.csv", start_val=1000000, commission=9.95, impact=0.005):
    """  		  	   		   	 			  		 			 	 	 		 		 	
    Computes the portfolio values.  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    :param orders_file: Path of the order file or the file object  		  	   		   	 			  		 			 	 	 		 		 	
    :type orders_file: str or file object  		  	   		   	 			  		 			 	 	 		 		 	
    :param start_val: The starting value of the portfolio  		  	   		   	 			  		 			 	 	 		 		 	
    :type start_val: int  		  	   		   	 			  		 			 	 	 		 		 	
    :param commission: The fixed amount in dollars charged for each transaction (both entry and exit)  		  	   		   	 			  		 			 	 	 		 		 	
    :type commission: float  		  	   		   	 			  		 			 	 	 		 		 	
    :param impact: The amount the price moves against the trader compared to the historical data at each transaction  		  	   		   	 			  		 			 	 	 		 		 	
    :type impact: float  		  	   		   	 			  		 			 	 	 		 		 	
    :return: the result (portvals) as a single-column dataframe, containing the value of the portfolio for each trading day in the first column from start_date to end_date, inclusive.  		  	   		   	 			  		 			 	 	 		 		 	
    :rtype: pandas.DataFrame  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    # this is the function the autograder will call to test your code  		  	   		   	 			  		 			 	 	 		 		 	
    # NOTE: orders_file may be a string, or it may be a file object. Your  		  	   		   	 			  		 			 	 	 		 		 	
    # code should work correctly with either input  		  	   		   	 			  		 			 	 	 		 		 	
    # TODO: Your code here  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	

    # read in dataframe
    order_df = pd.read_csv(orders_file, index_col="Date", parse_dates=True, na_values=['nan'])

    # read dates
    start_date = order_df.index[0]
    end_date = order_df.index[-1]

    # add more columns
    order_df["cash_after_order"] = np.nan
    order_df["port_val"] = np.nan
    order_df["stock_price"] = np.nan

    # create a table to track stock owned
    share_df = pd.DataFrame(columns=["Symbol", "Shares"])

    # get list of stock symbols
    stock_list = list(order_df.Symbol.unique())
    # store daily price for each stock
    price = {}
    for stock in stock_list:
        price[stock] = get_data([stock], pd.date_range(start_date, end_date)).ffill().bfill()

    # list of days and portval
    portvals = get_data(['SPY'], pd.date_range(start_date, end_date), addSPY=True, colname = 'Adj Close')

    # combine portvals df and order df into 1 df
    combined_df = portvals.join(order_df)

    # change index to numerical
    combined_df.reset_index(inplace=True)
    combined_df.rename(columns={"index":"Date"}, inplace=True)

    # loop through data
    for i in range(len(combined_df["Order"])):
        indexing = combined_df.at[i, 'Date']
        Symbol = combined_df.at[i, 'Symbol']
        Order = combined_df.at[i, 'Order']
        Share = combined_df.at[i, 'Shares']
        if Symbol not in stock_list:
            combined_df.at[i, "cash_after_order"] = float(combined_df.at[i - 1, "cash_after_order"])
            equity = 0
            for j in range(len(share_df.index)):
                equity += float(share_df.at[j, "Shares"]) * float(price[share_df.at[j, "Symbol"]].at[indexing, share_df.at[j, "Symbol"]])
            combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
        if i == 0:
            if Order == "BUY":
                share_df.loc[len(share_df.index)] = [Symbol, Share]
                combined_df.at[i, "cash_after_order"] = float(start_val - commission - (1 + impact) * Share * float(price[Symbol].at[indexing, Symbol]))
                equity = 0
                for j in range(len(share_df.index)):
                    equity += float(share_df.at[j, "Shares"]) * float(price[share_df.at[j, "Symbol"]].at[indexing, share_df.at[j, "Symbol"]])
                combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
            if Order == "SELL":
                share_df.loc[len(share_df.index)] = [Symbol, Share * (-1)]
                combined_df.at[i, "cash_after_order"] = float(start_val - commission + (1 - impact) * Share * float(price[Symbol].at[indexing, Symbol]))
                equity = 0
                for j in range(len(share_df.index)):
                    equity += float(share_df.at[j, "Shares"]) * float(price[share_df.at[j, "Symbol"]].at[indexing, share_df.at[j, "Symbol"]])
                combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
        else:

            if (Symbol not in list(share_df['Symbol'])) & (Symbol in stock_list):
                share_df.loc[len(share_df.index)] = [Symbol, 0]
            if Order == "BUY":
                share_df.loc[(share_df["Symbol"] == Symbol), "Shares"] += Share
                combined_df.at[i, "cash_after_order"] = float(combined_df.at[i - 1, "cash_after_order"]) - commission - float((1 + impact) * Share * float(price[Symbol].at[indexing, Symbol]))
                equity = 0
                for j in range(len(share_df.index)):
                    equity += float(share_df.at[j, "Shares"]) * float(price[share_df.at[j, "Symbol"]].at[indexing, share_df.at[j, "Symbol"]])
                combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
            if Order == "SELL":
                share_df.loc[(share_df["Symbol"] == Symbol), "Shares"] -= Share
                combined_df.at[i, "cash_after_order"] = float(combined_df.at[i - 1, "cash_after_order"]) - commission + float((1 - impact) * Share * float(price[Symbol].at[indexing, Symbol]))
                equity = 0
                for j in range(len(share_df.index)):
                    equity += float(share_df.at[j, "Shares"]) * float(price[share_df.at[j, "Symbol"]].at[indexing, share_df.at[j, "Symbol"]])
                combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity

    # portfolio value
    combined_df.set_index("Date", inplace=True)
    for day in combined_df.index:
        if isinstance(combined_df.loc[day], pd.DataFrame):
            same_day_df = combined_df.loc[day]
            same_day_df.reset_index(inplace=True)
            last_row = same_day_df.loc[len(same_day_df)-1]
            portvals.loc[day, 'value'] = last_row["port_val"]
        else:
            portvals.loc[day, 'value'] = combined_df.loc[day, "port_val"]
    portvals.drop(columns=["SPY"], inplace=True)

    return portvals

  		  	   		   	 			  		 			 	 	 		 		 	
def test_code():  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    Helper function to test code  		  	   		   	 			  		 			 	 	 		 		 	
    """  		  	   		   	 			  		 			 	 	 		 		 	
    # this is a helper function you can use to test your code  		  	   		   	 			  		 			 	 	 		 		 	
    # note that during autograding his function will not be called.  		  	   		   	 			  		 			 	 	 		 		 	
    # Define input parameters  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    of = "./orders/orders-01.csv"
    sv = 1000000  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    # Process orders  		  	   		   	 			  		 			 	 	 		 		 	
    portvals = compute_portvals(orders_file=of, start_val=sv, commission=9.95, impact=0.005)
    if isinstance(portvals, pd.DataFrame):  		  	   		   	 			  		 			 	 	 		 		 	
        portvals = portvals[portvals.columns[0]]  # just get the first column  		  	   		   	 			  		 			 	 	 		 		 	
    else:  		  	   		   	 			  		 			 	 	 		 		 	
        "warning, code did not return a DataFrame"  		  	   		   	 			  		 			 	 	 		 		 	
  		  	   		   	 			  		 			 	 	 		 		 	
    # Get portfolio stats  		  	   		   	 			  		 			 	 	 		 		 	
    # read in dataframe
    order_df = pd.read_csv(of, index_col="Date", parse_dates=True, na_values=['nan'])

    # read dates
    start_date = order_df.index[0]
    end_date = order_df.index[-1]
    cum_ret = portvals[len(portvals)-1] / portvals[0] - 1
    daily_return = portvals / portvals.shift(1) - 1
    daily_return = daily_return.iloc[1:]
    avg_daily_ret = daily_return.mean()  # average daily return
    std_daily_ret = daily_return.std()  # standard deviation of daily returns
    sharpe_ratio = np.sqrt(252) * avg_daily_ret / std_daily_ret  # sharp ratio

    #cum_ret_SPY, avg_daily_ret_SPY, std_daily_ret_SPY, sharpe_ratio_SPY = [0.2, 0.01, 0.02, 1.5]
  		  	   		   	 			  		 			 	 	 		 		 	

    # Compare portfolio against $SPX  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Date Range: {start_date} to {end_date}")  		  	   		   	 			  		 			 	 	 		 		 	
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Sharpe Ratio of Fund: {sharpe_ratio}")  		  	   		   	 			  		 			 	 	 		 		 	
    #print(f"Sharpe Ratio of SPY : {sharpe_ratio_SPY}")
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Cumulative Return of Fund: {cum_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    #print(f"Cumulative Return of SPY : {cum_ret_SPY}")
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Standard Deviation of Fund: {std_daily_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    #print(f"Standard Deviation of SPY : {std_daily_ret_SPY}")
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Average Daily Return of Fund: {avg_daily_ret}")  		  	   		   	 			  		 			 	 	 		 		 	
    #print(f"Average Daily Return of SPY : {avg_daily_ret_SPY}")
    print()  		  	   		   	 			  		 			 	 	 		 		 	
    print(f"Final Portfolio Value: {portvals[len(portvals)-1]}")

  		  	   		   	 			  		 			 	 	 		 		 	
def author():
    return 'fyan40'

if __name__ == "__main__":
    test_code()  		  	   		   	 			  		 			 	 	 		 		 	
