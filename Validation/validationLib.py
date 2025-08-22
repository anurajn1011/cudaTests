from DataProcessing import DataProcessing
import statistics

from Modeling.Modeling import normalizeTimeSeries
# dates

def backtest(algoName, strategySpecificArgs) :
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
    
    results = []
    # TODO this for loop is sus, s1 and s2 might not be addresable to open column in this way
    for stock1Data, stock2Data in zip(series1['open'], series2['open']):
        strategySpecificArgs = algoName((stock1Data,stock2Data), strategySpecificArgs)

    strategySpecificArgs["percentChange"] = (strategySpecificArgs["SharesOwnedT1"]+ strategySpecificArgs["SharesOwnedT2"] + strategySpecificArgs["cashWallet"])/initialValue
    return strategySpecificArgs
        


# TODO need to 'buy'/sell shares by using the cashWallet value
def CoIntStdDiv(newData, strategySpecificArgs):
    s1Data, s2Data  = newData
    pair = CoIntStdDivPair("s1", "s2")
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

    stock1PriceMA, stock1Std = pair.getStock1Stats() 
    stock2PriceMA, stock2Std = pair.getStock2Stats()
    
    # Signal Generation-------------------------------------
    #Enter Short Position: If Z>Upper Threshold, short the spread (sell outperforming asset, buy underperforming asset).
    if zScore>upperBound: # is opposite
        # is stock2pricefrom last 20 point > 1 std deviation of only stock2 and we have holding then buy
        if stock2PriceMA > stock2Std and  strategySpecificArgs["SharesOwnedT2"] > 0: #change references to use pairs
            strategySpecificArgs["SharesOwnedT2"] += 1 
        # is stock1pricefrom last 20 point > 1 std deviation of only stock1 and we have holding then sell
        if stock1PriceMA > stock1Std and  strategySpecificArgs["SharesOwnedT1"] <= 0: #change references to use pairs
            strategySpecificArgs["SharesOwnedT1"] -= 1
    #Enter Long Position: If Z<Lower Threshold, long the spread (buy underperforming asset, sell outperforming asset).
    if zScore<lowerBound:#stock2 is over performing or stock1 is underperforming
        # is stock2pricefrom last 20 point > 1 std deviation of only stock2 and we have holding then sell
        if stock2PriceMA > stock2Std and  strategySpecificArgs["SharesOwnedT2"] > 0:#change references to use pairs
            strategySpecificArgs["SharesOwnedT2"] -= 1
        # is stock1pricefrom last 20 point > 1 std deviation of only stock1 and we have holding then buy
        if stock1PriceMA > stock1Std and  strategySpecificArgs["SharesOwnedT1"] <= 0: #change references to use pairs
            strategySpecificArgs["SharesOwnedT1"] += 1

    #Exit Position: If Z reverts to within the exit thresholds or approaches zero, close the position.

    # TODO wtf was this for
    # when the diffrenece between the stock falls sout of bouynds buy or sell 
    if newMovingAverage < lowerBound and strategySpecificArgs["SharesOwnedT1"] :
        return (strategySpecificArgs["movingAvgSeries"]) 

    return (strategySpecificArgs)

class CoIntStdDivPair:
     def __init__(self, maLen ):
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
            self.maSeriesS1.append(ticker1NewData)
            self.maSeriesS2.append(ticker2NewData)
            self.maSeriesS1S2.append(ticker1NewData-ticker2NewData) #TODO check with Anuraj, I remember smthn about MA being negative for combined but unsure
            # Calc MAVals S1,S2, S1S2  
            self.maSeriesS1Val  =  sum(self.maSeriesS1)/len(self.maSeriesS1)
            self.maSeriesS2Val  =  sum(self.maSeriesS2)/len(self.maSeriesS2)
            self.maS1S2Val  =  sum(self.maSeriesS1S2)/len(self.maSeriesS1S2)
            # Calc stddivS1,stddivS2, stddivS1S2 and ZscoreS1S2
            self.stddivS1 = statistics.stdev(self.maSeriesS1)
            self.stddivS2 = statistics.stdev(self.maSeriesS2)
            self.stddivS1S2 = statistics.stdev(self.maSeriesS1S2)

        # Gets stock1 MA and Std
        def getStock1Stats():
            return (self.maSeriesS1Val, self.stddivS1)

        # Gets stock2 MA and Std
        def getStock2Stats():
            return (self.maSeriesS2Val, self.stddivS2)
        
        def getPairsMALen():
            return (len(self.maSeriesS1), len(self.maSeriesS2))

        # Gets  zScore, stdDiv, movingAvg for both stocks
        # TODO Anuraj calc zscore
        def getCoIntStdDivStats():
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

