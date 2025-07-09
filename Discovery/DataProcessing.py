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
from AlpacaDataGetter import AlpacaDataGetter

# AlphaVantage
# alphaVantageAPIKey = os.getenv("ALPHAVANTAGE_KEY")

# ts = TimeSeries(key=alphaVantageAPIKey, output_format='pandas')
# data, metaData = ts.get_intraday(symbol='TSLA', interval='1min', outputsize='full')
# data.index = pd.to_datetime(data.index)
# targetDate = "2025-07-03"
# filteredData = data[data.index.date == pd.to_datetime(targetDate).date()]
# print(filteredData)

# analyzer = AlpacaDataGetter()

# df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\nasdaq_screener.csv')
# sampling 100 random rows from df and storing it in new dataset, batch 00
# df_new = df.sample(n=100, random_state=40)
# df_new.to_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\sample_hundred_nasdaq_00.csv', index=False)

    
# df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\sample_hundred_nasdaq_00.csv')
# start, end = setTime(7, 3, 2025)

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

class DataProcessing(AlpacaDataGetter):
    def __init__(self):
        super().__init__()
    
    def read_data_to_DF(self, filename: str) -> pd.DataFrame:
        ''' 
            Load csv to pandas df 
        '''

        df = pd.read_csv(filename)
        return df
    
    def sampling_data_num_rows(self, dataframe: pd.DataFrame, samples: int, state: int) -> pd.DataFrame:
        ''' 
            Withdraw n rows from the df and provide a seed for the random state 
        '''

        df = dataframe.sample(n=samples, random_state=state)
        return df
    
    def set_time(self, month: int, day: int, year: int) -> Iterable[datetime]:
        ''' 
            Return a single day -- Alpaca Deals in UTC
        '''

        start_of_day = datetime(year, month, day, 13, 0) 
        end_of_day = start_of_day + timedelta(days=1)
        if start_of_day.month != end_of_day.month:
            if start_of_day.year != end_of_day.year:
                end_of_day = datetime(year + 1, 1, 1, 21, 0)
            else:
                end_of_day = datetime(year, month + 1, 1, 21, 0)
        return (start_of_day, end_of_day)
    
    def drop_rows(self, series1: pd.DataFrame, series2: pd.DataFrame) -> Iterable[pd.DataFrame]:
        ''' 
            Remove the rows which both Time Series do not share, returning a uniform number of rows between two assets and re-indexing them appropriately.
        '''
        
        # timestampsSeries1 = series1.index.get_level_values('timestamp')
        # timestampsSeries2 = series2.index.get_level_values('timestamp')
        # series1 = series1[timestampsSeries1.isin(timestampsSeries2)]
        # series2 = series2[timestampsSeries2.isin(timestampsSeries1)]
        # return (series1, series2)

        series1 = series1['open'].reset_index(level='symbol', drop=True)
        series2 = series2['open'].reset_index(level='symbol', drop=True)
        return series1.align(series2, join='inner')