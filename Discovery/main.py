from engle_granger import meanSquaredDistance
from DataProcessing import DataProcessing
import pandas as pd

alpaca = DataProcessing()
start, end = alpaca.set_time(7, 3, 25)

def pairSelection(ticker1, ticker2):

    # matching rows
    series1, series2 = alpaca.get_symbol_history(ticker1, start, end), alpaca.get_symbol_history(ticker2, start, end)
    series1, series2 = alpaca.drop_rows(series1, series2)
    mse = meanSquaredDistance(series1, series2)
    return mse

def main():
    df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\nasdaq_screener.csv')

    # pair selection via mse
    for i in range(len(df)):
        if df.iloc[i, 0].isalpha():
            series1 = alpaca.get_symbol_history(df.iloc[i, 0], start, end)
            print("Line 23")

        # type checks
        if isinstance(series1, pd.DataFrame):
            if 'open' not in series1.columns:
                print(f"\t'open' column missing in series2 for {df.iloc[i, 0]}, skipping.")
                continue
            series1 = series1['open'].reset_index(level='symbol', drop=True)
            print("Line 31")
        elif isinstance(series1, pd.Series):
            # Already a Series, no 'open' column to extract
            series1 = series1.reset_index(level='symbol', drop=True)
            print("Line 35")
        else:
            print(f"\tUnexpected data type for series2: {type(series1)}, skipping.")
            print("Line 38")
            continue

        for j in range(i + 1, len(df)):
            if df.iloc[j, 0].isalpha():
                series2 = alpaca.get_symbol_history(df.iloc[j, 0], start, end)
                print(f"MSE of {df.iloc[i, 0]} and {df.iloc[j, 0]} is: {pairSelection(series1, series2)}")

if __name__ == "main":
    main()