To get results/plots of the report, run testproject.py in python3.
It will give results and plots for both part 1 - indicators and part 2 - theoretical optimal strategy.

To change parameters:
	change window_size for each indicator in part_1 function in testproject.py:
		sma(start_day=start_day, end_day=end_day, symbol=symbol, plot=True, window_size=20)
	change symbol, sd, ed, sv in report function in testproject.py:
    	sd = dt.datetime(2008, 1, 1)
    	ed = dt.datetime(2009,12,31)
    	symbol = 'JPM'
    	sv = 100000

