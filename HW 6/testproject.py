"""
implement the necessary calls (following each respective API) to indicators.py and TheoreticallyOptimalStrategy.py,
 with the appropriate parameters to run everything needed for the report in a single Python call.
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
from indicators import sma, Bollinger_Bands, Momentum, ema, macd
import TheoreticallyOptimalStrategy as tos

pd.plotting.register_matplotlib_converters()

# part_1 indicators
def part_1(start_day, end_day, symbol):
    # plot sma
    sma(start_day=start_day, end_day=end_day, symbol=symbol, plot=True, window_size=20)

    # plot Bollinger_Bands
    Bollinger_Bands(start_day=start_day, end_day=end_day, symbol=symbol, plot=True, window_size=20)

    # plot Momentum
    Momentum(start_day=start_day, end_day=end_day, symbol=symbol, plot=True, window_size=20)

    # plot ema
    ema(start_day=start_day, end_day=end_day, symbol=symbol, plot = True, window_size = 20)

    # plot macd
    macd(start_day=start_day, end_day=end_day, symbol=symbol, plot = True)



# part 2 TheoreticallyOptimalStrategy
def part_2(df_trades, symbol, sd, ed, sv):
    # get df_trades value
    theoretical_vals = compute_portvals(orders_df=df_trades, start_val=sv, commission=0.00, impact=0.00)['port_val']


    # get benchmark value
    benchmark = get_data([symbol], pd.date_range(sd, ed)).ffill().bfill().drop(columns=['SPY'])
    benchmark[:] = 0
    benchmark.at[benchmark.index[0], symbol] = 1000
    benchmark_vals = compute_portvals(benchmark, sv, commission=0.00, impact=0.00)['port_val']


    # stats:
        # Cumulative return of the benchmark and portfolio
        # Stdev of daily returns of benchmark and portfolio
        # Mean of daily returns of benchmark and portfolio

    # Cumulative Return
    cum_ret_benchmark = (benchmark_vals[len(benchmark_vals) - 1] / benchmark_vals[0]) - 1
    cum_ret_theoretical = (theoretical_vals[len(theoretical_vals) - 1] / theoretical_vals[0]) - 1

    # Daily return
    daily_return_benchmark = (benchmark_vals / benchmark_vals.shift(1) - 1).iloc[1:]
    daily_return_theoretical = (theoretical_vals / theoretical_vals.shift(1) - 1).iloc[1:]

    # Stdev of daily returns
    std_daily_ret_benchmark = daily_return_benchmark.std()
    std_daily_ret_theoretical = daily_return_theoretical.std()

    # Mean of daily returns
    avg_daily_ret_benchmark = daily_return_benchmark.mean()
    avg_daily_ret_theoretical = daily_return_theoretical.mean()

    # print stats
    print("")
    print("[Benchmark]")
    print("Cumulative return: " + str(cum_ret_benchmark))
    print("Stdev of daily returns: " + str(std_daily_ret_benchmark))
    print("Mean of daily returns: " + str(avg_daily_ret_benchmark))
    print("")
    print("[TheoreticallyOptimalStrategy]")
    print("Cumulative return: " + str(cum_ret_theoretical))
    print("Stdev of daily returns: " + str(std_daily_ret_theoretical))
    print("Mean of daily returns: " + str(avg_daily_ret_theoretical))
    print("")


    # plot theoretical vs benchmark

    # normalize
    normalized_benchmark_vals = benchmark_vals / benchmark_vals[0]
    normalized_theoretical_vals = theoretical_vals / theoretical_vals[0]

    #plot
    plt.figure(figsize=(10, 6))
    plt.title("Theoretically Optimal Strategy")
    plt.xlabel("Date")
    plt.ylabel("Cumulative Return")
    plt.xticks(rotation=30)
    plt.grid()
    plt.plot(normalized_benchmark_vals, label="Benchmark", color="green")
    plt.plot(normalized_theoretical_vals, label="Theoritical", color="red")
    plt.legend()
    plt.savefig("Theoretical.png")
    #plt.show()
    plt.clf()


def report():
    sd = dt.datetime(2008, 1, 1)
    ed = dt.datetime(2009,12,31)
    symbol = 'JPM'
    sv = 100000

    # get df_trades from TOS
    df_trades = tos.testPolicy(symbol = "JPM", sd=dt.datetime(2008, 1, 1), ed=dt.datetime(2009,12,31), sv = 100000)

    part_1(start_day=sd, end_day=ed, symbol=symbol)
    part_2(df_trades = df_trades, symbol = symbol, sd = sd, ed = ed, sv = sv)

def author():
    return 'fyan40'

if __name__ == "__main__":
    report()
