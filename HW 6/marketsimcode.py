'''Student Name: Fanrui Yan (replace with your name)
GT User ID: fyan40 (replace with your User ID)
GT ID: 903660974 (replace with your GT ID)  	'''


import datetime as dt
import os
import numpy as np
import pandas as pd
from util import get_data, plot_data

pd.set_option('float_format', '{:f}'.format)
def compute_portvals(orders_df, start_val, commission, impact):
    order_df=orders_df

    # read dates
    start_date = order_df.index[0]
    end_date = order_df.index[-1]

    # add more columns
    order_df["cash_after_order"] = np.nan
    order_df["port_val"] = np.nan

    # track stock owned
    share_ownd = 0

    # get stock symbols
    Symbol = orders_df.columns[0]

    # store daily price for stock
    price = get_data([Symbol], pd.date_range(start_date, end_date)).ffill().bfill()

    # combine portvals = order_df
    combined_df = order_df

    # change index to numerical
    combined_df.reset_index(inplace=True)
    combined_df.rename(columns={"index": "Date"}, inplace=True)

    # loop through data
    for i in range(len(combined_df.index)):
        indexing = combined_df.at[i, 'Date']

        share_ownd += combined_df.at[i, Symbol]

        if combined_df.at[i, Symbol] == float(0):
            combined_df.at[i, "cash_after_order"] = float(combined_df.at[i - 1, "cash_after_order"])
            equity = share_ownd * float(price.at[indexing, Symbol])
            combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
        else:
            if combined_df.at[i, Symbol] < 0:
                Order = 'SELL'
                Share = abs(combined_df.at[i, Symbol])
            else:
                Order = 'BUY'
                Share = combined_df.at[i, Symbol]

        if i == 0:
            if Order == "BUY":
                combined_df.at[i, "cash_after_order"] = float(start_val - commission - (1 + impact) * Share * float(price.at[indexing, Symbol]))
                equity = share_ownd * float(price.at[indexing, Symbol])
                combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
            if Order == "SELL":
                combined_df.at[i, "cash_after_order"] = float(start_val - commission + (1 - impact) * Share * float(price.at[indexing, Symbol]))
                equity = share_ownd * float(price.at[indexing, Symbol])
                combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
        else:
            if Order == "BUY":
                combined_df.at[i, "cash_after_order"] = float(combined_df.at[i - 1, "cash_after_order"]) - commission - float((1 + impact) * Share * float(price.at[indexing, Symbol]))
                equity = share_ownd * float(price.at[indexing, Symbol])
                combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
            if Order == "SELL":
                combined_df.at[i, "cash_after_order"] = float(combined_df.at[i - 1, "cash_after_order"]) - commission + float((1 - impact) * Share * float(price.at[indexing, Symbol]))
                equity = share_ownd * float(price.at[indexing, Symbol])
                combined_df.at[i, "port_val"] = float(combined_df.at[i, "cash_after_order"]) + equity
        Order = ''
        Share = 0

    # portfolio value
    combined_df.set_index("Date", inplace=True)
    portvals = combined_df[["port_val"]]

    return portvals


def author():
    return 'fyan40'


if __name__ == "__main__":
    test_code()
