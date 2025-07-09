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


df = pd.read_csv('sample_hundred_nasdaq_00.csv')

alpaca = DataProcessing()
start, end = alpaca.set_time(7, 3, 2025)

for stock in df['Symbol']:
    
    series1 = alpaca.get_symbol_history(stock, start, end)
    

    X, Y = alpaca.drop_rows(series1, series2)
    Y = sm.add_constant(Y)

    # performing OLS with X, Y
    test = sm.OLS(X, Y).fit()
    print("The residuals at each time step: ", test.resid)
    print("Alpha and beta of OLS respectively: \n", test.params)
    
    res = adf(stock)