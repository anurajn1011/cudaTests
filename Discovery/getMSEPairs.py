import csv
from datetime import datetime
from engle_granger import meanSquaredDistance, adf
from DataProcessing import DataProcessing
import pandas as pd

alpaca = DataProcessing()
start = datetime(2024, 1, 1, 13, 0) 
end = datetime(2025, 1, 1, 13, 0) 

# filter stocks based on stationarity
def filterStockForStationarity(df, output_file):
    dataframe = pd.DataFrame()
    data_list = []
    for i in range(517, len(df)):
        if not isinstance(df.iloc[i, 0], float) and df.iloc[i, 0].isalpha():
            print(f"{df.iloc[i, 0]} is the current stock being assessed for Stationarity: ")
            series = alpaca.get_symbol_history(df.iloc[i, 0], start, end)
            if isinstance(series, pd.DataFrame):
                if 'open' not in series.columns:
                    print(f"\t'open' column missing in series, skipping.")
                    continue
                series = series['open'].reset_index(level='symbol', drop=True)
            elif isinstance(series, pd.Series):
                # Already a Series, no 'open' column to extract
                series = series.reset_index(level='symbol', drop=True)
            else:
                print(f"\tUnexpected data type for series, skipping.")
                continue
            try:
                if adf(series):
                    data_list.append(df.iloc[i, 0])
            except Exception as e:
                print(data_list)
                print(f"Its correpsonding series: {series}")
                print(f"An unexpected error occurred: {e}")
    print(data_list)
    print(f"An unexpected error occured: {e}")
    dataframe['tickers'] = data_list
    dataframe.to_csv(output_file, index=False)

# Selecting pairs and writes out to a CSV 
def generateStockPair2CSV_MSE(df, output_file, threshold=5) -> None:
    data_batch = {}
    for i in range(len(df)):
        if df.iloc[i, 1].isalpha():
            series1 = alpaca.get_symbol_history(df.iloc[i, 1], start, end)
        # type checks
        if isinstance(series1, pd.DataFrame):
            if 'open' not in series1.columns:
                print(f"\t'open' column missing in series1 for {df.iloc[i, 1]}, skipping.")
                continue
            series1 = series1['open'].reset_index(level='symbol', drop=True)
        elif isinstance(series1, pd.Series):
            # Already a Series, no 'open' column to extract
            series1 = series1.reset_index(level='symbol', drop=True)
        else:
            print(f"\tUnexpected data type for series1: {type(series1)}, skipping.")
            continue

        for j in range(i + 1, len(df)):
            if df.iloc[j, 1].isalpha():
                series2 = alpaca.get_symbol_history(df.iloc[j, 1], start, end)
                if series2.empty:
                    print(f"\tSeries2 for {df.iloc[j, 1]} is empty, skipping.")
                    continue  # skip to next j
                # checks to ensure that data is handled correctly
                if isinstance(series2, pd.DataFrame):
                    if 'open' not in series2.columns:
                        print(f"\t'open' column missing in series2 for {df.iloc[j, 1]}, skipping.")
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
                print(df.iloc[i, 1], df.iloc[j, 1])
                series1, series2 = series1.align(series2, join='inner')
                mse = meanSquaredDistance(series1, series2)
                if mse < threshold:
                    print(f"MSE of {df.iloc[i, 1]} and {df.iloc[j, 1]} is: {mse}")
                    data_batch[df.iloc[i, 1]] = (df.iloc[j, 1], mse)
                    writer(output_file, data_batch)
        

# 'C:\Users\User\Documents\Projects\cudaTests\results\nasdaq_screener_MSE.csv'
def writer(filename, data_batch) -> None:
     with open(filename, "a", newline="") as f:
        w = csv.writer(f)
        for index, (key, value) in enumerate(data_batch.items()):
            w.writerow([index, key] + list(value))

def main():
    data_batch = {}
    an_df_raw = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\nasdaq_screener.csv')
    an_stationarityFilter = r"C:\Users\User\Documents\Projects\cudaTests\CleanedData\nasdaq_screener_filtered_for_stationarity.csv"
    an_MSE = r"C:\Users\User\Documents\Projects\cudaTests\results\cleaned_nasdaq_screener_MSE.csv"
    # jo_df = pd.read_csv(r'C:\Users\jco10\Documents\PersonalProjects\cudaWAnuraj\cudaTests\datasets\constituents.csv')


    filterStockForStationarity(an_df_raw, an_stationarityFilter)
    an_df_cleaned = pd.read_csv(an_stationarityFilter)
    generateStockPair2CSV_MSE(an_df_cleaned, an_MSE)

    ''' Step 1: pair selection via mse '''
    # generateStockPair2CSV_MSE(df, r"C:\Users\User\Documents\Projects\cudaTests\results\constituents_MSE.csv")
    # generateStockPair2CSV_MSE(df, r"C:\Users\jco10\Documents\PersonalProjects\cudaWAnuraj\cudaTests\results\constituents_MSE.csv")

if __name__ == "__main__":
    main()

       
