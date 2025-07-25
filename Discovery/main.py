import pandas as pd
import datetime
from getMSEPairs import filterStockForStationarity, generateStockPair2CSV_MSE
from CoIntegrationTestLoop import testStockPairForCoInt

def main():
    # start = datetime(2024, 1, 1, 13, 0) 
    # end = datetime(2025, 1, 1, 13, 0) 
    
    # check for stationarity
    # an_df_raw = pd.read_csv(r'C:\Users\User\Documents\Projects\cudaTests\datasets\nasdaq_screener.csv')
    # an_stationarityFilter = r"C:\Users\User\Documents\Projects\cudaTests\CleanedData\nasdaq_screener_filtered_for_stationarity.csv"
    jc_stationarityFilter = r"C:\Users\jco10\Documents\PersonalProjects\cudaWAnuraj\cudaTests\CleanedData\nasdaq_screener_filtered_for_stationarity.csv"
    # filterStockForStationarity(an_df_raw, an_stationarityFilter)

    # check pairs that satisfy MSE constraints
    df_cleaned = pd.read_csv(jc_stationarityFilter)
    # an_MSE = r"C:\Users\User\Documents\Projects\cudaTests\results\cleaned_nasdaq_screener_MSE.csv"
    jc_MSE = r"C:\Users\jco10\Documents\PersonalProjects\cudaWAnuraj\cudaTests\results\cleaned_nasdaq_screener_MSE.csv"
    generateStockPair2CSV_MSE(df_cleaned, jc_MSE)

    # run the cointegration testloop
    # testStockPairForCoInt(an_MSE, start, end)

if __name__ == "__main__":
    main()