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
  		   	  			  	 		  		  		    	 		 		   		 		  
Student Name: Jie Lyu	   	  			  	 		  		  		    	 		 		   		 		  
GT User ID: jlyu31			  	 		  		  		    	 		 		   		 		  
GT ID: 903329676		   	  			  	 		  		  		    	 		 		   		 		  
"""  		   	  		

"""

    [Run this file]
PYTHONPATH=../:. python3 marketsim.py

    [Run grading scripts]
PYTHONPATH=../:. python3 grade_marketsim.py

"""
  		   	  			  	 		  		  		    	 		 		   		 		  
import pandas as pd  		   	  			  	 		  		  		    	 		 		   		 		  
import numpy as np  		   	  			  	 		  		  		    	 		 		   		 		  
import datetime as dt  		   	  			  	 		  		  		    	 		 		   		 		  
import os  		   	  			  	 		  		  		    	 		 		   		 		  
from util import get_data, plot_data  		   	  			  	 		  		  		    	 		 		   		 		  

                           
                           	  	 		  		  		    	 		 		   		 		  
def compute_portvals(orders_file = "./orders/orders.csv", start_val = 1000000, commission=9.95, impact=0.005):  		   	  			  	 		  		  		    	 		 		   		 		  
    # this is the function the autograder will call to test your code  		   	  			  	 		  		  		    	 		 		   		 		  
    # NOTE: orders_file may be a string, or it may be a file object. Your  		   	  			  	 		  		  		    	 		 		   		 		  
    # code should work correctly with either input  		   	  			  	 		  		  		    	 		 		   		 		  
    # TODO: Your code here

    ##### setting up
    orders_df = pd.read_csv(orders_file, index_col='Date', parse_dates=True, na_values=['nan'])
    start_date, end_date, orders_dates = get_dates(orders_df)

    # wrong
    portvals = get_data(['SPY'], pd.date_range(start_date, end_date), addSPY=True, colname = 'Adj Close')
    portvals = portvals.rename(columns={'SPY': 'value'})
    dates = portvals.index

    ##### my account
    current_cash = start_val
    shares_owned = {}           # symbol (str) -> number (int)
    symbol_table = {}        # symbol (str) -> prices (pd.df)

    ##### going through dates
    for date in dates:

        if date in orders_dates:
            # date is <class 'pandas._libs.tslibs.timestamps.Timestamp'>
            # details is <class 'pandas.core.series.Series'>
            details = orders_df.loc[date]

            # if there are multiple orders on the same day
            if isinstance(details, pd.DataFrame):
                for _,each in details.iterrows():
                    symbol = each.loc['Symbol']
                    order = each.loc['Order']
                    shares = each.loc['Shares']
                    current_cash, shares_owned, symbol_table = \
                        update_share_cash(symbol, order, shares, current_cash, shares_owned, symbol_table, date, end_date, commission, impact)
            # if there is only one order on that day
            else:
                symbol = details.loc['Symbol']
                order = details.loc['Order']
                shares = details.loc['Shares']

                current_cash, shares_owned, symbol_table = \
                    update_share_cash(symbol, order, shares, current_cash, shares_owned, symbol_table, date, end_date, commission, impact)
        
        ### calculating current protfolio value
        portvals.loc[date].loc['value'] = compute_portval(date, current_cash, shares_owned, symbol_table)

    return portvals  		    



"""########
Helper functions for compute_portvals
"""########


# returns the start_date, end_date and orders_dates
def get_dates(orders_df):
    orders_dates = orders_df.index
    start_date = orders_df.index[0]
    end_date = orders_df.index[-1]
    return start_date, end_date, orders_dates


# update current_cash and shares_owned from an order
def update_share_cash(symbol, order, shares, current_cash, shares_owned, symbol_table, curr_date, end_date, commission, impact):

    # if we have not loaded the symbol information yet
    if symbol not in symbol_table:
        # get the df for the symbol
        symbol_df = get_data([symbol], pd.date_range(curr_date, end_date), addSPY=True, colname = 'Adj Close')  
        # back fill and forward fill missing informations on market opend dates
        symbol_df = symbol_df.ffill().bfill()
        # add the symbol df to symbol_table
        symbol_table[symbol] = symbol_df
        # print(type(symbol_table[symbol]))


    # update the share and cash information
    if order == 'BUY':
        share_change = shares
        cash_change = -symbol_table[symbol].loc[curr_date].loc[symbol] * (1 + impact) * shares
    elif order == 'SELL':
        share_change = -shares
        cash_change = symbol_table[symbol].loc[curr_date].loc[symbol] * (1 - impact) * shares
    else:
        print('ERROR: unknow order type')

    print(shares_owned.get(symbol, 0))
    shares_owned[symbol] = shares_owned.get(symbol, 0) + share_change
    current_cash += cash_change - commission

    return current_cash, shares_owned, symbol_table


# compute the portfolio value for a day
def compute_portval(curr_date, current_cash, shares_owned, symbol_table):
    shares_worth = 0
    for symbol in shares_owned:
        shares_worth += symbol_table[symbol].loc[curr_date].loc[symbol] * shares_owned[symbol]
    return current_cash + shares_worth


"""########
end of helper functions
"""########

  		   	  			  	 		  		  		    	 		 		   		 		  
def test_code():  		   	  			  	 		  		  		    	 		 		   		 		  
    # this is a helper function you can use to test your code  		   	  			  	 		  		  		    	 		 		   		 		  
    # note that during autograding his function will not be called.  		   	  			  	 		  		  		    	 		 		   		 		  
    # Define input parameters  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    of = "./orders/orders-01.csv"
    sv = 1000000  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # Process orders  		   	  			  	 		  		  		    	 		 		   		 		  
    portvals = compute_portvals(orders_file = of, start_val = sv)  		   	  			  	 		  		  		    	 		 		   		 		  
    if isinstance(portvals, pd.DataFrame):  		   	  			  	 		  		  		    	 		 		   		 		  
        portvals = portvals[portvals.columns[0]] # just get the first column  		   	  			  	 		  		  		    	 		 		   		 		  
    else:  		   	  			  	 		  		  		    	 		 		   		 		  
        "warning, code did not return a DataFrame"  

    print(portvals)		   	  			  	 		  		  		    	 		 		   		 		  

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
    return 'jlyu31'
	  			  	 		  		  		    	 		 		   		 		  
if __name__ == "__main__":  		   	  			  	 		  		  		    	 		 		   		 		  
    test_code()  		   	  			  	 		  		  		    	 		 		   		 		  



"""
    # In the template, instead of computing the value of the portfolio, we just  		   	  			  	 		  		  		    	 		 		   		 		  
    # read in the value of IBM over 6 months  		   	  			  	 		  		  		    	 		 		   		 		  
    # start_date = dt.datetime(2008,1,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    # end_date = dt.datetime(2008,6,1)  		   	  			  	 		  		  		    	 		 		   		 		  
    # portvals = get_data(['IBM'], pd.date_range(start_date, end_date))  		   	  			  	 		  		  		    	 		 		   		 		  
    # portvals = portvals[['IBM']]  # remove SPY  		   	  			  	 		  		  		    	 		 		   		 		  
    # rv = pd.DataFrame(index=portvals.index, data=portvals.values)  		   	  			  	 		  		  		    	 		 		   		 		  
  		   	  			  	 		  		  		    	 		 		   		 		  
    # return rv  
"""