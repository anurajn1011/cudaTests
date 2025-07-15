import csv
from datetime import datetime
from engle_granger import meanSquaredDistance
from DataProcessing import DataProcessing
import pandas as pd

alpaca = DataProcessing()
start = datetime(2024, 1, 1, 13, 0) 
end = datetime(2025, 1, 1, 13, 0) 

def pairSelection(df, output_file, threshold=5) -> None:
    data_batch = {}
    for i in range(len(df)):
        if df.iloc[i, 0].isalpha():
            series1 = alpaca.get_symbol_history(df.iloc[i, 0], start, end)
        # type checks
        if isinstance(series1, pd.DataFrame):
            if 'open' not in series1.columns:
                print(f"\t'open' column missing in series1 for {df.iloc[i, 0]}, skipping.")
                continue
            series1 = series1['open'].reset_index(level='symbol', drop=True)
        elif isinstance(series1, pd.Series):
            # Already a Series, no 'open' column to extract
            series1 = series1.reset_index(level='symbol', drop=True)
        else:
            print(f"\tUnexpected data type for series1: {type(series1)}, skipping.")
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
                mse = pairSelection(series1, series2)
                if mse < threshold:
                    mse = meanSquaredDistance(series1, series2)
                    print(f"MSE of {df.iloc[i, 0]} and {df.iloc[j, 0]} is: {mse}")
                    data_batch[df.iloc[i, 0]] = df.iloc[j, 0]
    writer(output_file, data_batch)

# 'C:\Users\User\Documents\Projects\cudaTests\results\nasdaq_screener_MSE.csv'
def writer(filename, data_batch) -> None:
     with open(filename, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(['index', 'key', 'value'])
        for index, (key, value) in enumerate(data_batch.items()):
            w.writerow([index, key] + list(value))

def main():
    data_batch = {}
    df = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\sample_hundred_nasdaq_00.csv')

    ''' Step 1: pair selection via mse '''
    pairSelection(df)

if __name__ == "__main__":
    main()