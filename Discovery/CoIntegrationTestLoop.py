import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm
from engle_granger import adf, OLSResiduals, coIntegrationTest
from DataProcessing import DataProcessing

'''
    Step 1: Validate for the expected stationarity/heteroscedacity of individual assets via ADF
    Step 2: Perfom an Ordinary Least Squares(OLS) regression of one asset on the other
    Step 3: Validate the residuals on the ADF, verifying for I(1)
'''


df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\sample_hundred_nasdaq_00.csv')

alpaca = DataProcessing()
start, end = alpaca.set_time(7, 3, 2025)

for i in range(len(df)):
    if '^' not in df.iloc[i, 0]:
        series1 = alpaca.get_symbol_history(df.iloc[i, 0], start, end)
        series1 = series1['open'].reset_index(level='symbol', drop=True)
        for j in range(i + 1, len(df)):
            series2 = alpaca.get_symbol_history(df.iloc[j, 0], start, end)
            series2 = series2['open'].reset_index(level='symbol', drop=True)
            print(df.iloc[i, 0], df.iloc[j, 0])
            series1, series2 = series1.align(series2, join='inner')
            boolSeries1, boolSeries2 = adf(series1), adf(series2)
            if not boolSeries1 and not boolSeries2:
                residuals = OLSResiduals(series1, series2)
                boolCoIntegrated = coIntegrationTest(residuals)