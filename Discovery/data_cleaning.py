import os
import numpy as np
import pandas as pd
import csv
from datetime import date, datetime, timedelta
from statsmodels.tsa.stattools import coint, adfuller

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
from Analysis import AlpacaDataGetter

load_dotenv()

# AlphaVantage
alphaVantageAPIKey = os.getenv("ALPHAVANTAGE_KEY")

# Alpaca
apiKey = os.getenv("ALPACA_KEY")
secretKey= os.getenv("ALPACA_SECRET")
stock_client = StockHistoricalDataClient(apiKey, secretKey)

# ts = TimeSeries(key=alphaVantageAPIKey, output_format='pandas')
# data, metaData = ts.get_intraday(symbol='TSLA', interval='1min', outputsize='full')
# data.index = pd.to_datetime(data.index)
# targetDate = "2025-07-03"
# filteredData = data[data.index.date == pd.to_datetime(targetDate).date()]
# print(filteredData)

# reading the data
analyzer = AlpacaDataGetter()
df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\nasdaq_screener.csv')
df_tail = df.tail(5012)
df_head = df.head(100)
# time range
start_of_day = datetime(2025, 7, 3, 13, 0)
end_of_day   = datetime(2025, 7, 4, 21, 0)

# finding all tickers with every minute filled
tickerSet = set()
for name in df_tail['Symbol']:
    if '$' in name or '^' in name or '/' in name:
        continue
    stockSymbolHistory = analyzer.get_symbol_history(name.strip(), start_of_day, end_of_day)
    if stockSymbolHistory.shape[0] >= 478:
        tickerSet.add(name)
        print("Added new ticker to the set: ", tickerSet)
    print("Ticker Name: ", name)

print("Completed set: ", tickerSet)

stockSymbolHistory = analyzer.get_symbol_history('WOLF', start_of_day, end_of_day)
print(stockSymbolHistory)

# checking each ticker for stationarity
# stationarity = adfuller(time_series)
# print('ADF Statistic:', result[0])
# print('p-value:', result[1])
