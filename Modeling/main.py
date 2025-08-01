import datetime 
from DataProcessing import DataProcessing
from Modeling import calculationOfSpread


alpaca = DataProcessing()


def main():
    # Test input =======
    series1Ticker, series2Ticker = "ACDC","AIRJ"
    # ==================
    start = datetime.datetime(2025,1,10,13,0) 
    end = datetime.datetime(2025, 1, 10, 22, 0) 
    series1 = alpaca.get_symbol_history(series1Ticker, start, end)
    series2 = alpaca.get_symbol_history(series2Ticker, start, end)
    # print(series1)
    calculationOfSpread(series1,series2)


if __name__ == "__main__":
    main()