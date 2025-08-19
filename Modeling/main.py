import datetime 
from DataProcessing import DataProcessing
from Modeling import calculationOfSpread, normalizeTimeSeries
import numpy as np
import statsmodels.api as sm
from statsmodels.tsa.stattools import adfuller
from sklearn.metrics import mean_squared_error
import pandas as pd
import json


alpaca = DataProcessing()


def main():
    # Test input =======
    # series1Ticker, series2Ticker = "ACDC","AIRJ"
    # ==================
    start = datetime.datetime(2025,8,1,13,0) 
    end = datetime.datetime(2025, 8, 1, 21, 0) 
    
    df = pd.read_csv(r"results/cointegrated_pairs_nasdaq_screener_postMSE.csv")
    params_data = []
    testing = input("Test run? (Enter \"Yes\"): ")
    testingBool = True if testing.lower() == "yes" else False

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
        spreadTrain_t = spreadTrainSet.iloc[:-1].to_frame().reset_index(drop=True)
        spreadTrain_t_plus_one = spreadTrainSet.iloc[1:].to_frame().reset_index(drop=True)

        # Step 3: train and fit a GLS model
        model = sm.GLS(endog=spreadTrain_t_plus_one, exog=sm.add_constant(spreadTrain_t, has_constant="add"))
        model_res = model.fit()
        print(model_res.summary())

        # Step 4: Evaluate the model on test data
        spreadTest_t = spreadTestSet.iloc[:-1].to_frame().reset_index(drop=True)
        spreadTest_t_plus_one = spreadTestSet.iloc[1:].to_frame().reset_index(drop=True)
        predict = model.predict(params=model_res.params, exog=sm.add_constant(spreadTest_t, has_constant="add"))
        mse = mean_squared_error(spreadTest_t_plus_one, predict)
        print(f"The mse of the prediction made by the model for {stock1} and {stock2} is {mse}")

        # Step 5: Check that the residuals are stationary, if so we add them to our params_data
        try:
            adf = adfuller(model_res.resid)
            if adf[1] < 0.05:
                print("Residuals are stationary, this is a strong pair to work with.")
            else:
                print("Residuals are NOT stationary, continue.")
                continue
        except ValueError:
            print("Residuals are near constant, minimal standard deviation. Trivially stationary.")
            
        # Step 5: Saving the model params
        params = {
            "intercept": float(model_res.params.iloc[0]),
            "slope": float(model_res.params.iloc[1]),
            "mse": float(mse),
            "ticker1": stock1,
            "ticker2": stock2
        }
        params_data.append(params)

        # allow manual parse
        if testingBool:
            userInput = input("Press 1 to continue to the next iteration, 0 to break: ")
            while userInput not in ("0", "1"):
                userInput = input("INVALID; Enter 1 to continue, 0 otherwise: ")
            if userInput == "0":
                break

    # Saving model params to JSON
    with open(r"results/model_results/model_params.json", "w") as fd:
        json.dump(params_data, fd, indent=3)
    

if __name__ == "__main__":
    main()