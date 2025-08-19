import datetime 
from DataProcessing import DataProcessing
from Modeling import calculationOfSpread, normalizeTimeSeries
import numpy as np
import statsmodels.api as sm
from sklearn.metrics import mean_squared_error
import pandas as pd


alpaca = DataProcessing()


def main():
    # Test input =======
    # series1Ticker, series2Ticker = "ACDC","AIRJ"
    # ==================
    start = datetime.datetime(2025,8,1,13,0) 
    end = datetime.datetime(2025, 8, 1, 21, 0) 
    
    df = pd.read_csv(r"results/cointegrated_pairs_nasdaq_screener_postMSE.csv")
    rows_data = []
    testingBool = True

    for col, row in df.iterrows():
        stock1, stock2 = row["key"], row["value"]
        series1 = alpaca.get_symbol_history(stock1, start, end)
        series2 = alpaca.get_symbol_history(stock2, start, end)
        # print("STATS " + row["key"] + " " + row["value"] + "===============================================================")
        if len(series1) < 1 or len(series2) < 1:
            continue
        # print(series1)
        # Normalize time series indexes
        # series1 = normalizeTimeSeries(series1, start)

        # Step 1: Calculate the spread of the two shares
        spread = calculationOfSpread(series1,series2)

        # Exponential Moving Average
        # ema = spread.ewm(com=0.2, min_periods=1200).mean()
        # print("EMA:\n", ema)

        # Step 2: Split the spread into a training and testing dataset.
        trainSize = int(len(spread) * 0.8)
        spreadTrainSet = spread.iloc[:trainSize]
        spreadTestSet = spread.iloc[trainSize:]
        spreadTrain_t = spreadTrainSet.iloc[:-1].reset_index(drop=True)
        spreadTrain_t_plus_one = spreadTrainSet.iloc[1:].reset_index(drop=True)

        # Step 3: train and fit a GLS model
        model = sm.GLS(endog=spreadTrain_t_plus_one, exog=sm.add_constant(spreadTrain_t))
        model_res = model.fit()
        print(model_res.summary())

        # Step 4: Evaluate the model on test data
        spreadTest_t = spreadTestSet.iloc[:-1]
        spreadTest_t_plus_one = spreadTestSet.iloc[1:]
        predict = model.predict(params=model_res.params, exog=sm.add_constant(spreadTest_t))
        mse = mean_squared_error(spreadTest_t_plus_one, predict)
        print(f"The mse of the prediction made by the model for {stock1} and {stock2} is {mse}")
        
        
        # rows_data.append({"ticker1": row["key"] , "ticker2":row["value"]})

        # allow manual parse
        if testingBool:
            userInput = input("Press 1 to continue to the next iteration, 0 to break: ")
            while userInput not in ("0", "1"):
                userInput = input("INVALID; Enter 1 to continue, 0 otherwise: ")
            if userInput == "0":
                break

    # pd.DataFrame(rows_data).to_csv('cointegrated_pairs_scores.csv', index=False)
    

if __name__ == "__main__":
    main()