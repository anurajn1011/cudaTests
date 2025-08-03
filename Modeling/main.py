import datetime 
from DataProcessing import DataProcessing
from Modeling import calculationOfSpread, normalizeTimeSeries


alpaca = DataProcessing()


def main():
    # Test input =======
    series1Ticker, series2Ticker = "ACDC","AIRJ"
    # ==================
    start = datetime.datetime(2025,8,1,13,0) 
    end = datetime.datetime(2025, 8, 1, 22, 0) 
    series1 = alpaca.get_symbol_history(series1Ticker, start, end)
    series2 = alpaca.get_symbol_history(series2Ticker, start, end)

    # Normalize time series indexes
    series1 = normalizeTimeSeries(series1, start)

    print(series1)
    # calculationOfSpread(series1,series2)




if __name__ == "__main__":
    main()