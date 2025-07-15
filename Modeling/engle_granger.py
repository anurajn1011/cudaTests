# File for Engle-Granger Test - 7/9/25

import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm
from DataProcessing import DataProcessing
import sys
sys.path.append('../')
'''
    Step 1: Validate for the expected stationarity/heteroscedacity of individual assets via ADF
    Step 2: Perfom an Ordinary Least Squares(OLS) regression of one asset on the other
    Step 3: Validate the residuals on the ADF, verifying for I(1)
'''

def adf(series) -> bool:
    '''
        In the case of Engle-Granger, two time series are provided. Each are independently checked for heteroscedasticity.
        The method adfuller returns a tuple: (test statistic, p-value, used lag, number of observations, critical values, maximized information criterion).
        H0: Time Series has a unit root (Non-Stationary)
        H1: Time Series does not have a unit root (Stationary)
        Confidence Level of 95% and p < 0.05 for rejection
    '''
    res = adfuller(series)
    if res[1] < 0.05:
        print(f"We can reject the Null Hypothesis. Asset has a p-value of {res[1]} and a test statistic of {res[0]} less than the corresponding critical value at 5% of {res[4]['5%']}.\n")
        return True
    print(f"Failed to reject the Null Hypothesis. Asset has a p-value of {res[1]} and a test statistic of {res[0]} with corresponding critical value at 5% of {res[4]['5%']}.\n")
    return False

def OLSResiduals(series1, series2):
    alpaca = DataProcessing()
    # series1, series2 =  alpaca.drop_rows(series1, series2)
    series2 = sm.add_constant(series2)
    test = sm.OLS(series1, series2).fit()
    print("The residuals at each time step: ", test.resid)
    print("Alpha and beta of OLS respectively: \n", test.params) # alpha - intercept, beta - slope
    return test.resid


def coIntegrationTest(residuals):
    res = adfuller(residuals)
    if res[1] < 0.05:
        print(f"CO-INTEGRATED !We can reject the Null Hypothesis. The a p-value of {res[1]} and a test statistic of {res[0]} less than the corresponding critical value at 5% of {res[4]['5%']}.\n")
        return True
    print(f"NOT CO-INTEGRATED !Failed to reject the Null Hypothesis. The has a p-value of {res[1]} and a test statistic of {res[0]} with corresponding critical value at 5% of {res[4]['5%']}.\n")
    return False


'''
    series1 = alpha + beta*series2 + residuals
'''

# alpaca = DataProcessing()
# start, end = alpaca.set_time(7, 3, 2025)

# series1 = alpaca.get_symbol_history("TSLA", start, end)
# series2 = alpaca.get_symbol_history("AAPL", start, end)

# X, Y = alpaca.drop_rows(series1, series2)
# Y = sm.add_constant(Y)



# # checking for the stationarity of the OLS Residuals
# residuals = test.resid
# sol = adf(res=residuals)