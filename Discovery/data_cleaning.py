import os
import numpy as np
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

stock_client = StockHistoricalDataClient(apiKey, secretKey)

''' Necessary Modules '''

def get_timeframe():
    tf_unit = TimeFrameUnit("Min")
    return TimeFrame(1, tf_unit)

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

# reading the data
df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\nyse-listed.csv')

# time range
start_of_day = datetime(2025, 7, 3, 13, 0)
end_of_day   = datetime(2025, 7, 4, 21, 0)

# finding all tickers with every minute filled
tickerSet = set()
for name in df['ACT Symbol']:
    if '$' in name:
        continue
    stockSymbolHistory = get_symbol_history(name, start_of_day, end_of_day)
    if stockSymbolHistory.shape[0] == 479:
        tickerSet.add(name)
    print(name)

print(tickerSet)

# result = adfuller(time_series)
# print('ADF Statistic:', result[0])
# print('p-value:', result[1])
