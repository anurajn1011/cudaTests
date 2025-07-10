import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm
from engle_granger import adf
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
        for j in range(i + 1, len(df)):
            series2 = alpaca.get_symbol_history(df.iloc[j, 0], start, end)
            bool1, bool2 = adf(stock1=series1, stock2=series2)
            if not bool1 and not bool2:
                X, Y = alpaca.drop_rows(series1, series2)
                Y = sm.add_constant(Y)
                # performing OLS with X, Y
                test = sm.OLS(X, Y).fit()
                result = adf(residual=test.resid)
    # print("The residuals at each time step: ", test.resid)
    # print("Alpha and beta of OLS respectively: \n", test.params)
    
    # res = adf(stock)