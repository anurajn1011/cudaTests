import datetime 
from validationLib import backtest, normalizeTimeSeries
import numpy as np
import statsmodels.api as sm
import pandas as pd


alpaca = DataProcessing()


def main():
    # This should ideally output a saved csv with columns algoName, ticker1, ticker2, startDate, endDate,initialValue, finalValue, percent change
    
    # Test input =======
    series1Ticker, series2Ticker = "ACDC","AIRJ"
    start = datetime.datetime(2025,8,1,13,0) 
    end = datetime.datetime(2025, 8, 1, 21, 0) 
    # ==================
    df1 = 0
    df2 = 0


    for i in range(0,10):
        df1 = backtest(algo1, "input2", "algoinput1")
        df2 = backtest(algo1, "input4", "algoinput5")
        dfAll = df1+df2
    SavedfAll = dfAll
        

if __name__ == "__main__":
    main()

# The core of the backtesting loop works by drip feeding data 1 point at a time to an algo that decides if on the new data point it should buy or sell