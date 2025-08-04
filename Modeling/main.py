import datetime 
from DataProcessing import DataProcessing
from Modeling import calculationOfSpread, normalizeTimeSeries
import numpy as np
import statsmodels.api as sm


alpaca = DataProcessing()


def main():
    # Test input =======
    series1Ticker, series2Ticker = "ACDC","AIRJ"
    # ==================
    start = datetime.datetime(2025,8,1,13,0) 
    end = datetime.datetime(2025, 8, 1, 21, 0) 
    series1 = alpaca.get_symbol_history(series1Ticker, start, end)
    series2 = alpaca.get_symbol_history(series2Ticker, start, end)
    # print(series1)
    # Normalize time series indexes
    # series1 = normalizeTimeSeries(series1, start)

    # Step 1: Calculate the spread of the two shares
    spread = calculationOfSpread(series1,series2)

    # Step 2: Exponential Moving Average
    ema = spread.ewm(com=0.2, min_periods=1200).mean()
    # print("EMA:\n", ema)

    # Step 3: Obtain the Upper and Lower bounds of the moving average; +/- 1 STD
    spread_t = spread.iloc[0 : len(spread) - 1]
    spread_t = spread_t.reset_index(drop=True)
    spread_t_plus_1 = spread.iloc[1 : len(spread)]
    spread_t_plus_1 = spread_t_plus_1.reset_index(drop=True)
    model = sm.GLS(endog=spread_t_plus_1, exog=spread_t)
    model_res = model.fit()
    print(model_res.summary())


if __name__ == "__main__":
    main()