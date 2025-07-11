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

import numpy as np
import matplotlib.pyplot as plt

from stochastic.processes.diffusion.vasicek import OrnsteinUhlenbeckProcess
import matplotlib.pyplot as plt

# Create an OU process instance
ou = OrnsteinUhlenbeckProcess(speed=0.7, vol=0.06, t=1)

# Sample the process (defaults to 1000 steps)
sample_path = ou.sample()

# Plot it
plt.plot(sample_path)
plt.title("Ornstein-Uhlenbeck Process")
plt.xlabel("Time step")
plt.ylabel("X_t")
plt.show()

