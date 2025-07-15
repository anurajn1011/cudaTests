import pandas as pd
from statsmodels.tsa.stattools import coint, adfuller
import statsmodels.api as sm
from engle_granger import adf, OLSResiduals, coIntegrationTest
from DataProcessing import DataProcessing
import warnings
import csv

'''
    Step 1: Validate for the expected stationarity/heteroscedacity of individual assets via ADF
    Step 2: Perfom an Ordinary Least Squares(OLS) regression of one asset on the other
    Step 3: Validate the residuals on the ADF, verifying for I(1)
'''


df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\nasdaq_screener.csv')

alpaca = DataProcessing()
start, end = alpaca.set_time(7, 3, 2025)

data_batch_00 = {}

# cointegration
for i in range(len(df)):
    if df.iloc[i, 0].isalpha():
        series1 = alpaca.get_symbol_history(df.iloc[i, 0], start, end)
        # type checks
        if isinstance(series1, pd.DataFrame):
                if 'open' not in series1.columns:
                    print(f"\t'open' column missing in series2 for {df.iloc[i, 0]}, skipping.")
                    continue
                series1 = series1['open'].reset_index(level='symbol', drop=True)
        elif isinstance(series1, pd.Series):
            # Already a Series, no 'open' column to extract
            series1 = series1.reset_index(level='symbol', drop=True)
        else:
            print(f"\tUnexpected data type for series2: {type(series1)}, skipping.")
            continue
        for j in range(i + 1, len(df)):
            if df.iloc[j, 0].isalpha():
                series2 = alpaca.get_symbol_history(df.iloc[j, 0], start, end)

                if series2.empty:
                    print(f"\tSeries2 for {df.iloc[j, 0]} is empty, skipping.")
                    continue  # skip to next j
                # checks to ensure that data is handled correctly
                if isinstance(series2, pd.DataFrame):
                    if 'open' not in series2.columns:
                        print(f"\t'open' column missing in series2 for {df.iloc[j, 0]}, skipping.")
                        continue
                    series2 = series2['open'].reset_index(level='symbol', drop=True)
                elif isinstance(series2, pd.Series):
                    # Already a Series, no 'open' column to extract
                    series2 = series2.reset_index(level='symbol', drop=True)
                else:
                    print(f"\tUnexpected data type for series2: {type(series2)}, skipping.")
                    continue
                if len(series1) <= 20 or len(series2) <= 20:
                    break
                print(df.iloc[i, 0], df.iloc[j, 0])
                series1, series2 = series1.align(series2, join='inner')
                # possibility of being nearly colinear, handle of such cases
                with warnings.catch_warnings():
                    warnings.simplefilter("error")
                    try:
                        score, p_value, critical_vals = coint(series1, series2)
                        if p_value < 0.05:
                            print(f"\t{df.iloc[i, 0]} AND {df.iloc[j, 0]} ARE COINTEGRATED SERIES! P-Value: {p_value}, Score: {score}, and Critical Values: {critical_vals}")
                            data_batch_00[df.iloc[i, 0]] = [df.iloc[j, 0], p_value, score, critical_vals]
                    except:
                        print(f"\tWarning caught: {Warning}")

# converting data to csv
with open(r'C:\Users\User\Documents\Projects\cudaTests\datasets\cointegration_pairs_nasdaq_screener.csv', "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(['index', 'key', 'value', 'p-value', 'test-statistic', 'critical-values'])
    for index, (key, value) in enumerate(data_batch_00.items()):
        w.writerow([index, key] + list(value))


# df.to_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\cointegration_pairs_sample_batch00.csv')

# for i in range(len(df)):
#     if '^' not in df.iloc[i, 0]:
#         series1 = alpaca.get_symbol_history(df.iloc[i, 0], start, end)
#         series1 = series1['open'].reset_index(level='symbol', drop=True)
#         for j in range(i + 1, len(df)):
#             series2 = alpaca.get_symbol_history(df.iloc[j, 0], start, end)
#             series2 = series2['open'].reset_index(level='symbol', drop=True)
#             if len(series1) <= 20 or len(series2) <= 20:
#                 break
#             print(df.iloc[i, 0], df.iloc[j, 0])
#             series1, series2 = series1.align(series2, join='inner')
#             boolSeries1, boolSeries2 = adf(series1), adf(series2)
#             if not boolSeries1 and not boolSeries2:
#                 residuals = OLSResiduals(series1, series2)
#                 boolCoIntegrated = coIntegrationTest(residuals)