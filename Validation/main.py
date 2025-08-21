import datetime 

import numpy as np
import statsmodels.api as sm
import pandas as pd
import statistics
from DataProcessing import DataProcessing


# The core of the backtesting loop works by drip feeding data 1 point at a time to an algo that decides if on the new data point it should buy or sell
def backTest(algoName, strategySpecificArgs):
    """Run a backtest given market data and trading signals. Returns a df with following columns"""
    # columns algoName, ticker1, ticker2, startDate, endDate,initialValue, finalValue, percent change
    # call dataProccessor to get array of data
    initialValue = strategySpecificArgs["cashWallet"]
    startDate = strategySpecificArgs["startDate"]
    endDate = strategySpecificArgs["endDate"]
    dataGetter = DataProcessing()
    series1 = dataGetter.get_symbol_history(strategySpecificArgs["ticker1"], startDate, endDate)
    series2 = dataGetter.get_symbol_history(strategySpecificArgs["ticker2"], startDate, endDate)
    
    series1 = normalizeTimeSeries(series1, startDate)
    series2 = normalizeTimeSeries(series2, startDate)
    
    for stock1Data, stock2Data in zip(series1['open'], series2['open']):
        strategySpecificArgs = algoName((stock1Data,stock2Data), strategySpecificArgs)

    strategySpecificArgs["percentChange"] = (strategySpecificArgs["SharesOwnedT1"]+ strategySpecificArgs["SharesOwnedT2"] + strategySpecificArgs["cashWallet"])/initialValue
    return strategySpecificArgs
        





def CoIntStdDiv(newData, strategySpecificArgs):
    s1Data, s2Data  = newData
    pair = CoIntStdDivPair()
    pair.addNewDataPoints(s1Data, s2Data)
    
    lenMASeriesS1, lenMASeriesS2 = pair.getPairsMALen()
    if lenMASeriesS1 < 1200 and lenMASeriesS2 < 1200:
        return (strategySpecificArgs)
    # take a moving avg over 1200 steps (20 min) 
    
    zScore, stdDiv, movingAvgVal = pair.getCoIntStdDivStats() # Gets stats    
    
    # set upper bound to stdiv + moving avg 
    upperBound = stdDiv + movingAvgVal # can stay just needs to change std_dev and newMA vars
    # set lower bound to stdiv - moving avg 
    lowerBound = stdDiv - movingAvgVal # can stay just needs to change std_dev and newMA vars

    stock1PriceMAVal, stock1Std = pair.getStock1Stats() 
    stock2PriceMAVal, stock2Std = pair.getStock2Stats()
    
    # Signal Generation-------------------------------------
    #Enter Short Position: If Z>Upper Threshold, short the spread (sell outperforming asset, buy underperforming asset).
    if zScore>upperBound: # is opposite
        # is stock2pricefrom last 20 point > 1 std deviation of only stock2 and we have holding then buy
        if s1Data > stock2Std + stock2PriceMAVal  and  strategySpecificArgs["SharesOwnedT1"] > 0 and strategySpecificArgs["cashWallet"] > s2Data: #change references to use pairs
            newShares = strategySpecificArgs["cashWallet"] // s2Data
            strategySpecificArgs["SharesOwnedT2"] += newShares
            strategySpecificArgs["cashWallet"] -= newShares*s2Data
        # is stock1pricefrom last 20 point > 1 std deviation of only stock1 and we have holding then sell
        if s2Data > stock1Std - stock1PriceMAVal and  strategySpecificArgs["SharesOwnedT1"] <= 0 : #change references to use pairs
            newCash = strategySpecificArgs["SharesOwnedT1"]*s1Data
            strategySpecificArgs["SharesOwnedT1"] = 0
            strategySpecificArgs["cashWallet"] += newCash
    #Enter Long Position: If Z<Lower Threshold, long the spread (buy underperforming asset, sell outperforming asset).
    if zScore<lowerBound:#stock2 is over performing or stock1 is underperforming
        # is stock2pricefrom last 20 point > 1 std deviation of only stock2 and we have holding then sell
        if s1Data > stock2Std-stock2PriceMAVal and  strategySpecificArgs["SharesOwnedT2"] > 0 :#change references to use pairs
            newCash = strategySpecificArgs["SharesOwnedT2"] * s2Data
            strategySpecificArgs["SharesOwnedT2"] = 0 
            strategySpecificArgs["SharesOwnedT2"] += newCash
        # is stock1pricefrom last 20 point > 1 std deviation of only stock1 and we have holding then buy
        if s2Data > stock1Std - stock1PriceMAVal and  strategySpecificArgs["SharesOwnedT1"] <= 0 and strategySpecificArgs["cashWallet"] > s1Data: #change references to use pairs
            newShares = strategySpecificArgs["cashWallet"] // s1Data
            strategySpecificArgs["SharesOwnedT1"] += newShares
            strategySpecificArgs["cashWallet"] -= newShares*s1Data



    return (strategySpecificArgs)

# setup to inherit from data getter
class CoIntStdDivPair:
    def __init__(self,  ):
        # Instance variables (unique to each object) 
        self.maSeriesS1 = []
        self.maSeriesS2 = []
        self.maSeriesS1S2 = []
        self.maS1S2Val = 0
        self.maSeriesS1Val = 0
        self.maSeriesS2Val = 0
        self.stddivS1 = 0
        self.stddivS2 = 0
        self.stddivS1S2 = 0
        

        # Add new data points to stock1 and stock2 and calcs new stats
    def addNewDataPoints(self, ticker1NewData, ticker2NewData):
        # Append to MA
        if (len(self.maSeriesS1) < 1200):
            self.maSeriesS1.append(ticker1NewData)
            self.maSeriesS2.append(ticker2NewData)
            self.maSeriesS1S2.append(ticker1NewData-ticker2NewData)
        else:
            self.maSeriesS1.pop()
            self.maSeriesS2.pop()
            self.maSeriesS1S2.pop()
            self.maSeriesS1.append(ticker1NewData)
            self.maSeriesS2.append(ticker2NewData)
            self.maSeriesS1S2.append(ticker1NewData-ticker2NewData)            
            # Calc MAVals S1,S2, S1S2  
            self.maSeriesS1Val  =  sum(self.maSeriesS1)/len(self.maSeriesS1)
            self.maSeriesS2Val  =  sum(self.maSeriesS2)/len(self.maSeriesS2)
            self.maS1S2Val  =  sum(self.maSeriesS1S2)/len(self.maSeriesS1S2)
            # Calc stddivS1,stddivS2, stddivS1S2 and ZscoreS1S2
            self.stddivS1 = statistics.stdev(self.maSeriesS1)
            self.stddivS2 = statistics.stdev(self.maSeriesS2)
            self.stddivS1S2 = statistics.stdev(self.maSeriesS1S2)

    # Gets stock1 MA and Std
    def getStock1Stats(self):
        self.ma
        return (self.maSeriesS1Val, self.stddivS1)

    # Gets stock2 MA and Std
    def getStock2Stats(self):
        return (self.maSeriesS2Val, self.stddivS2)
    
    def getPairsMALen(self):
        return (len(self.maSeriesS1), len(self.maSeriesS2))

    # Gets  zScore, stdDiv, movingAvg for both stocks
    # TODO Anuraj calc zscore
    def getCoIntStdDivStats(self):
        '''
            Z = (spread_t - mu) / sigma; The mean and std can be computed using the model parameters,
            which follows from the discretization of the OU model. 

            Lambda: Speed of mean reversion
            Mu: mean 
            Sigma: std

            Given the discretized OU Model: S_(t+1) = aS_t + b + epsilon (Not Euler-Mauryama)
            lambda = -log(a)/delta(t) 
            mu = b/(1-a)
            sigma = std(epsilon) * sqrt((-2*log(a)) / (delta(t) * (1-a**2)))
        '''
        lam, mu, sigma = 0, 0, 0
        return (lam, mu, sigma)
        # return (0, self.stddivS1S2, self.maS1S2Val)

def normalizeTimeSeries(timeSeries, date):
    # Ensure timestamp is datetime and set index properly
    timeSeries = timeSeries.copy()
    timeSeries.index = pd.MultiIndex.from_tuples(
        [(symbol, pd.to_datetime(ts)) for symbol, ts in timeSeries.index],
        names=["symbol", "timestamp"]
    )

    normalizedFrames = []

    startTime = datetime.datetime.combine(date, datetime.time(13, 0, 0)).replace(tzinfo=datetime.timezone.utc)
    endTime = datetime.datetime.combine(date, datetime.time(21, 0, 0)).replace(tzinfo=datetime.timezone.utc)
    fullTimeRange = pd.date_range(start=startTime, end=endTime, freq='1s')
    initialPrice = timeSeries.head(1).iloc[0, 0]

    for symbol, group in timeSeries.groupby(level="symbol"):
        symbolDf = group.droplevel("symbol")
        reindexedDf = symbolDf.reindex(fullTimeRange)
        filledDf = reindexedDf.ffill()

        for col in ["open", "high", "low", "close"]:
            if col in filledDf.columns:
                filledDf[col] = filledDf[col].fillna(initialPrice)
        
        filledDf["symbol"] = symbol
        filledDf.set_index("symbol", append=True, inplace=True)
        filledDf.index.set_names(["timestamp", "symbol"], inplace=True)
        filledDf = filledDf.reorder_levels(["symbol", "timestamp"])
        normalizedFrames.append(filledDf)

    return pd.concat(normalizedFrames).sort_index()




def main():
    # This should ideally output a saved csv with columns algoName, ticker1, ticker2, startDate, endDate,initialValue, finalValue, percent change
    
    # Test input =======
    series1Ticker, series2Ticker = "ACDC","AIRJ"
    start = datetime.datetime(2025,8,1,13,0) 
    end = datetime.datetime(2025, 8, 1, 21, 0) 
    # ==================
    df1 = 0
    df2 = 0

    CoIntStdDivArgs1 = {"ticker1":"ACDC", "ticker2":"AIRJ", "cashWallet":1000 ,"startDate":datetime.datetime(2025,8,1,13,0), "endDate":datetime.datetime(2025, 8, 1, 21, 0), "SharesOwnedT1": 0, "SharesOwnedT2": 0} 
    CoIntStdDivArgs1 = backTest(CoIntStdDiv, CoIntStdDivArgs1)
    
    df1 = pd.DataFrame([CoIntStdDivArgs1])

    print(df1)
    
    
    
        

if __name__ == "__main__":
    main()
