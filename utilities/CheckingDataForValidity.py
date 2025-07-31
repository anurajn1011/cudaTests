import pandas as pd

def CheckingDataForValidity(**kwargs):
    for value in kwargs.items():
        if isinstance(value, pd.DataFrame):
            if 'open' not in value.columns:
                print(f"\t'open' column missing in series1 or series2, skipping.")
            return value['open'].reset_index(level='symbol', drop=True)
        elif isinstance(value, pd.Series):
            # Already a Series, no 'open' column to extract
            return value.reset_index(level='symbol', drop=True)
        else:
            print(f"\tUnexpected data type for series1 or series2, skipping.")
            return None