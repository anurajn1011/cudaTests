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

# Our Imports
from Discovery.AlpacaDataGetter import AlpacaDataGetter


'''
    For our model, since we intend on trading intraday per minute, we will utilize
    the Exponential Moving Average(EMA). The fundamental model is a naive pairs trading one, 
    modified using the Discretized Ornstein-Uhlenbleck Process. For further information, refer
    to the following article: https://arxiv.org/html/2412.12458v1
'''

# Step 1: For some time step, take the difference between the prices of cointegrated stocks
# Step 2: Take the Exponential Moving Average, with an appropriate window, of this spread.
# Step 3: To obtain the upper and lower signals for mean reversion, take the std.
# Step 4: We discretize the Ornstein-Uhlenbleck Process (Defining the future time, S_t+1, with the current S_t, where S is spread)
# Step 5: Run regression of S_t+1 on S_t, obtaining residuals along the way.
# Step 6: Calculate the Z-Scores


# Step 1
def calculationOfSpread(series1, series2):
    # The gist is series1['open'] - series2['open']

    # first, we check if the data being passed is acceptable
    if isinstance(series1, pd.DataFrame) and isinstance(series2, pd.DataFrame):
        if 'open' not in series1.columns or 'open' not in series2.columns:
            print(f"\t'open' column missing in series1 or series2, skipping.")
        series1 = series1['open'].reset_index(level='symbol', drop=True)
        series2 = series2['open'].reset_index(level='symbol', drop=True)
    elif isinstance(series1, pd.Series)  and isinstance(series2, pd.Series):
        # Already a Series, no 'open' column to extract
        series1 = series1.reset_index(level='symbol', drop=True)
        series2 = series2.reset_index(level='symbol', drop=True)
    else:
        print(f"\tUnexpected data type for series1 or series2, skipping.")

    # second, we then fill in missing data for either with the previous time step.
    