import os
import numpy as np
import pandas as pd
import csv
from datetime import date, datetime, timedelta
from statsmodels.tsa.stattools import coint, adfuller
from typing import Tuple, Iterable

# Alpaca imports
from alpaca_trade_api.rest import REST  # , TimeFrame, TimeFrameUnit
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import json
import backtrader as bt
import backtrader.feeds as btfeeds
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from dotenv import load_dotenv

# AlphaVantage Imports
from alpha_vantage.timeseries import TimeSeries

# Custom library of AlpacaData
from Discovery.AlpacaDataGetter import AlpacaDataGetter

# AlphaVantage
# alphaVantageAPIKey = os.getenv("ALPHAVANTAGE_KEY")

# ts = TimeSeries(key=alphaVantageAPIKey, output_format='pandas')
# data, metaData = ts.get_intraday(symbol='TSLA', interval='1min', outputsize='full')
# data.index = pd.to_datetime(data.index)
# targetDate = "2025-07-03"
# filteredData = data[data.index.date == pd.to_datetime(targetDate).date()]
# print(filteredData)

analyzer = AlpacaDataGetter()

# reading the data
def readDataToDF(filename) -> pd.DataFrame:
    df = pd.read_csv(filename)
    return df
# df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\nasdaq_screener.csv')

def samplingDataNumRows(dataframe, state) -> pd.DataFrame:
    df = dataframe.sample(n=100, random_state=state)
    return df
# sampling 100 random rows from df and storing it in new dataset, batch 00
# df_new = df.sample(n=100, random_state=40)
# df_new.to_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\sample_hundred_nasdaq_00.csv', index=False)

# time range, UTC
def setTime(month, day, year) -> Iterable[datetime, datetime]:
    start_of_day = datetime(year, month, day, 13, 0) 
    end_of_day = start_of_day + timedelta(days=1)
    if start_of_day.month != end_of_day.month:
        if start_of_day.year != end_of_day.year:
            end_of_day = datetime(year + 1, 1, 1, 21, 0)
        else:
            end_of_day = datetime(year, month + 1, 1, 21, 0)
    return (start_of_day, end_of_day)

# checking each ticker for stationarity
df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\sample_hundred_nasdaq_00.csv')

# stationarity = adfuller(time_series)
# print('ADF Statistic:', result[0])
# print('p-value:', result[1])

# finding all tickers with every minute filled
# tickerSet = set()
# for name in df['Symbol']:
#     if '$' in name or '^' in name or '/' in name:
#         continue
#     stockSymbolHistory = analyzer.get_symbol_history(name.strip(), start_of_day, end_of_day)
#     if stockSymbolHistory.shape[0] >= 478:
#         tickerSet.add(name)
#         print("Added new ticker to the set: ", tickerSet)
#     print("Ticker Name: ", name)

# print("Completed set: ", tickerSet)

# stockSymbolHistory = analyzer.get_symbol_history('WOLF', start_of_day, end_of_day)
# print(stockSymbolHistory)
