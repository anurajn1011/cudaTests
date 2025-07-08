from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.stattools import coint

from dateutil.relativedelta import relativedelta
import os
import config
import logging
import asyncio
import requests
import pandas as pd
import csv
from datetime import date, datetime, timedelta
from alpaca_trade_api.rest import REST  # , TimeFrame, TimeFrameUnit
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import json
import backtrader as bt
import backtrader.feeds as btfeeds
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from dotenv import load_dotenv


load_dotenv()




apiKey = os.getenv("ALPACA_KEY")
secretKey= os.getenv("ALPACA_SECRET")
print(apiKey)
print(secretKey)

stock_client = StockHistoricalDataClient(apiKey, secretKey)



def get_symbol_history(symbol, simulationStartDate, simulationEndDate):  # returns dataframe, symbol string, simulationStartDate string,
    # SimulationEndDate string
    # Converting string representation of dates to datetime objs for TimeFrame
    # datetime format
    # dtStartDate = string_to_datetime(simulationStartDate)
    # dtEndDate = string_to_datetime(simulationEndDate)
    dtStartDate = simulationStartDate
    dtEndDate = simulationEndDate
    # timeframe
    time_frame = get_timeframe()

    request_params = StockBarsRequest(
        symbol_or_symbols=[symbol],
        timeframe=TimeFrame.Minute,
        start=dtStartDate,
        end=dtEndDate,
    )
    symbol_bars = stock_client.get_stock_bars(request_params)
    return symbol_bars.df

# Convert string date to datetime date
def string_to_datetime(date):
    return datetime.strptime(date, "%Y-%m-%d")


# Create timeframe object
def get_timeframe():
    tf_unit = TimeFrameUnit("Min")
    return TimeFrame(1, tf_unit)


# Expected output format of get_symbol_history(symbol)
"""
symbol  		timestamp                		open  	    high	    low 	    close	    volume		    trade_count	    vwap
BTC/USD 	    2022-09-01 05:00:00+00:00   	20049.0 	20285.0	    19555.0 	20160.0 	2396.3504   	18060.0		    19920.278135
        		2022-09-02 05:00:00+00:00   	20159.0 	20438.0 	19746.0 	19924.0 	1688.0641   	16730.0 		20045.987764
        		2022-09-03 05:00:00+00:00   	19924.0 	19963.0 	19661.0 	19802.0 	624.1013    	9853.0  		19794.111057
		        2022-09-04 05:00:00+00:00   	19801.0 	20060.0 	19599.0 	19892.0 	1361.6668   	8489.0  		19885.445568
		        2022-09-05 05:00:00+00:00   	19892.0 	20173.0 	19640.0 	19762.0 	2105.0539   	11900.0 		19814.853546
		        2022-09-06 05:00:00+00:00   	19763.0 	20025.0 	18539.0 	18720.0 	3291.1657   	19591.0 		19272.505607
		        2022-09-07 05:00:00+00:00   	18723.0 	19459.0 	18678.0 	19351.0 	2259.2351   	16204.0 		19123.487500
"""

# ---------------------------------------------------------------------


target_date = datetime(2025, 7, 7) # Replace with your desired date

# Define the start and end of the day
# start_of_day = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
start_of_day = datetime(2025, 7, 3, 13, 0)
end_of_day   = datetime(2025, 7, 4, 21, 0)



stockSymbol_ge_hist = get_symbol_history("TSLA", start_of_day, end_of_day )
print(stockSymbol_ge_hist)


# # Testing moving averages
# movinAvgCross(100000, 5, 20, "SPY", "2021-12-01", "2023-01-15")
# movinAvgCross(100000, 5, 20, "GE", "2021-12-01", "2023-01-15" )

# time_series=stockSymbol_ge_hist["open"]
# series1=stockSymbol_ge_hist["open"]
# series2=stockSymbol_ge_hist["close"]

# # TODO
# result = adfuller(time_series)
# print('ADF Statistic:', result[0])
# print('p-value:', result[1])



# score, pvalue, _ = coint(series1, series2)
# print('Cointegration test statistic:', score)
# print('p-value:', pvalue)
