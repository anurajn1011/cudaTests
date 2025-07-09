# File for Engle-Granger Test - 7/9/25

import pandas as pd
from DataProcessing import DataProcessing
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm

'''
    Step 1: Validate for the expected stationarity/heteroscedacity of individual assets via ADF
    Step 2: Perfom an Ordinary Least Squares(OLS) regression of one asset on the other
    Step 3: Validate the residuals on the ADF, verifying for I(1)
'''

def adf(**kwargs) -> list:
    '''
        In the case of Engle-Granger, two time series are provided. Each are independently checked for heteroscedasticity.
        The method adfuller returns a tuple: (test statistic, p-value, used lag, number of observations, critical values, maximized information criterion).
        H0: Time Series has a unit root (Non-Stationary)
        H1: Time Series does not have a unit root (Stationary)
        Confidence Level of 95% and p < 0.05 for rejection
    '''
    condition = -1
    adfRes = []
    for key, series in kwargs.items():
        if series.empty:
            print(f"{key} has an empty series")
        else:
            res = adfuller(series)
            adfRes.append([key] + list(res))
            if res[1] < 0.05 and res[0] < res[4]['5%']:
                print(f"We can reject the Null Hypothesis. {key} has a p-value of {res[1]} and a test statistic of {res[0]} less than the corresponding critical value at 5% of {res[4]['5%']}.\n")
                condition = 0
            else:
                print(f"Failed to reject the Null Hypothesis. {key} has a p-value of {res[1]} and a test statistic of {res[0]} with corresponding critical value at 5% of {res[4]['5%']}.\n")
                condition = 1
    if len(adfRes) == 1:
        if condition == 1:
            print(f"{adfRes[0][0]} suggests that the two assets are not cointegrated.")
        else:
            print(f"As a consequence of the Engle-Granger Test {adfRes[0][0]} suggests that the two assets are cointegrated!")

    return adfRes


'''
    series1 = alpha + beta*series2 + residuals
'''

alpaca = DataProcessing()
start, end = alpaca.set_time(7, 3, 2025)

series1 = alpaca.get_symbol_history("TSLA", start, end)
series2 = alpaca.get_symbol_history("AAPL", start, end)

X, Y = alpaca.drop_rows(series1, series2)
Y = sm.add_constant(Y)

# performing OLS with X, Y
test = sm.OLS(X, Y).fit()
print("The residuals at each time step: ", test.resid)
print("Alpha and beta of OLS respectively: \n", test.params)

# checking for the stationarity of the OLS Residuals
residuals = test.resid
sol = adf(res=residuals)