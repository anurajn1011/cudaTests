import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm
from engle_granger import adf, OLSResiduals, coIntegrationTest
from DataProcessing import DataProcessing
import warnings
import csv
from datetime import datetime

'''
    Step 1: Validate for the expected stationarity/heteroscedacity of individual assets via ADF
    Step 2: Perfom an Ordinary Least Squares(OLS) regression of one asset on the other
    Step 3: Validate the residuals on the ADF, verifying for I(1)
'''

def testStockPairForCoInt(df, start, end):
    alpaca = DataProcessing()
    data_batch_00 = {}
    # cointegration
    for i in range(len(df)):
        if df.iloc[i, 1].isalpha() and df.iloc[i, 2].isalpha():
            series1 = alpaca.get_symbol_history(df.iloc[i, 1], start, end)
            series2 = alpaca.get_symbol_history(df.iloc[i, 2], start, end)
            # type checks
            if isinstance(series1, pd.DataFrame) and isinstance(series2, pd.DataFrame):
                    if 'open' not in series1.columns or 'open' not in series2.columns:
                        print(f"\t'open' column missing in series1 or series2, skipping.")
                        continue
                    series1 = series1['open'].reset_index(level='symbol', drop=True)
                    series2 = series2['open'].reset_index(level='symbol', drop=True)
            elif isinstance(series1, pd.Series)  and isinstance(series2, pd.Series):
                # Already a Series, no 'open' column to extract
                series1 = series1.reset_index(level='symbol', drop=True)
                series2 = series2.reset_index(level='symbol', drop=True)
            else:
                print(f"\tUnexpected data type for series1 or series2, skipping.")
                continue
            if not adf(series1) or not adf(series2):
                break
            series1, series2 = series1.align(series2, join='inner')
            # possibility of being nearly colinear, handle of such cases
            with warnings.catch_warnings():
                warnings.simplefilter("error")
                try:
                    score, p_value, critical_vals = coint(series1, series2)
                    print(score)
                    print(p_value)
                    print(critical_vals)
                    if p_value < 0.05:
                        print("pval < 0.05")
                        print(f"\t{df.iloc[i, 1]} AND {df.iloc[i, 2]} ARE COINTEGRATED SERIES! P-Value: {p_value}, Score: {score}, and Critical Values: {critical_vals}")
                        data_batch_00[df.iloc[i, 1]] = [df.iloc[i, 2], p_value, score, critical_vals]
                except:
                    print(f"\tWarning caught: {Warning}")

    # converting data to csv
    # with open(r'C:\Users\User\Documents\Projects\cudaTests\datasets\cointegration_pairs_nasdaq_screener.csv', "w", newline="") as f:
    with open(r'C:\Users\jco10\Documents\PersonalProjects\cudaWAnuraj\cudaTests\Results\cointegration_pairs_hogAndC.csv', "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(['index', 'key', 'value', 'p-value', 'test-statistic', 'critical-values'])
        for index, (key, value) in enumerate(data_batch_00.items()):
            w.writerow([index, key] + list(value))

def main():
    data_batch = {}
    df = pd.read_csv(r'C:\Users\jco10\Documents\PersonalProjects\cudaWAnuraj\cudaTests\results\constituents_MSE.csv')
    # df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\results\constituents_MSE.csv')


    start = datetime(2024, 1, 1, 13, 0) 
    end = datetime(2025, 1, 1, 13, 0) 

    ''' Step 1: Check MSE pairs for co-integration '''
    testStockPairForCoInt(df, start, end)
    

if __name__ == "__main__":
    main()
# df.to_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\cointegration_pairs_sample_batch00.csv')

# for i in range(len(df)):
#     if '^' not in df.iloc[i, 1]:
#         series1 = alpaca.get_symbol_history(df.iloc[i, 1], start, end)
#         series1 = series1['open'].reset_index(level='symbol', drop=True)
#         for j in range(i + 1, len(df)):
#             series2 = alpaca.get_symbol_history(df.iloc[j, 0], start, end)
#             series2 = series2['open'].reset_index(level='symbol', drop=True)
#             if len(series1) <= 20 or len(series2) <= 20:
#                 break
#             print(df.iloc[i, 1], df.iloc[j, 0])
#             series1, series2 = series1.align(series2, join='inner')
#             boolSeries1, boolSeries2 = adf(series1), adf(series2)
#             if not boolSeries1 and not boolSeries2:
#                 residuals = OLSResiduals(series1, series2)
#                 boolCoIntegrated = coIntegrationTest(residuals)