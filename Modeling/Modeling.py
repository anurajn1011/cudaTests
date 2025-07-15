import os
import numpy as np
import pandas as pd
import csv
from datetime import date, datetime, timedelta
from statsmodels.tsa.stattools import coint, adfuller
from statsmodels.regression.linear_model import GLS
from statsmodels.tools import add_constant

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
from engle_granger import OLSResiduals
import numpy as np
import matplotlib.pyplot as plt
from DataProcessing import DataProcessing

def main():
    df = pd.read_csv(r'C:\Users\jco10\Documents\PersonalProjects\cudaWAnuraj\cudaTests\results\cointegration_pairs_sample.csv')

    
    alpaca = DataProcessing()
    start, end = alpaca.set_time(7, 3, 2025)

    
    for key, value in df[['key', 'value']].to_numpy():
        # Step 1: OLS on two cointegrated assets to obtain residuals Z_t    
        print(key, value)
        series1 = alpaca.get_symbol_history(key, start, end)
        series2 = alpaca.get_symbol_history(value, start, end)
        series1,series2 = alpaca.drop_rows(series1, series2)
        residuals = OLSResiduals(series1=series1, series2=series2)  
        # Step 2: Compute delta Z_t by taking the differences of every element with its previous one
        deltaZ = residuals.diff().dropna()
        # Step 3: Regress delta Zt on z(t-1) via GLS.
        print(deltaZ)
        deltaZ = add_constant(deltaZ)
        print(deltaZ)
        zLag = residuals.iloc[1:]
        gls_model = GLS(deltaZ, zLag).fit()
        # print(gls_model.summary())
        break
        

    

if __name__ == "__main__":
    main()



