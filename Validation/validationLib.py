from DataProcessing import DataProcessing
import statistics
# dates

def backtest(algoName, strategySpecificArgs) :
    """Run a backtest given market data and trading signals. Returns a df with following columns"""
    # columns algoName, ticker1, ticker2, startDate, endDate,initialValue, finalValue, percent change
    datagett = DataProcessing
    
    results = []
    for price in data:
        signal = algoName(price, strategySpecificArgs)
        results.append((price, signal))
    return results
    pass
# TODO consider adding moving average class from crossover moving average trading algo
def CoIntStdDiv(newData, strategySpecificArgs):
    s1Data, s2Data  = newData
    pair = CoIntStdDivPair("s1", "s2")
    pair.addNewDataPoints(s1Data, s2Data)
    
    lenMASeriesS1, lenMASeriesS2 = pair.getPairsMALen()
    if lenMASeriesS1 < 1200 and lenMASeriesS2 < 1200:
        return (strategySpecificArgs)
    # take a moving avg over 1200 steps (20 min) 
    strategySpecificArgs["movingAvgSeries"]
    zScore, stdDiv, movingAvg = CoIntStdDivStats()
    # recalculate new moving avg
    movingAvgSeriesSum = sum(strategySpecificArgs["movingAvgSeries"])
    movingAvgSeriesLen = len(strategySpecificArgs["movingAvgSeries"])
    newMovingAverage  =  movingAvgSeriesSum/movingAvgSeriesLen
    # take stdiv of the moving avg
    std_dev = statistics.stdev(strategySpecificArgs["movingAvgSeries"])
    # set upper bound to stdiv + moving avg 
    upperBound = std_dev + newMovingAverage
    # set lower bound to stdiv - moving avg 
    lowerBound = std_dev - newMovingAverage

    stock1PriceMA = 1
    stock1Std = 1
    stock2PriceMA = 1
    stock2Std = 1
    # Signal Generation-------------------------------------
    #Enter Short Position: If Z>Upper Threshold, short the spread (sell outperforming asset, buy underperforming asset).
    if zScore>upperBound: # is opposite
        # is stock2pricefrom last 20 point > 1 std deviation of only stock2 and we have holding then buy
        if stock2PriceMA > stock2Std and  strategySpecificArgs["SharesOwnedT2"] > 0:
            strategySpecificArgs["SharesOwnedT2"] += 1
        # is stock1pricefrom last 20 point > 1 std deviation of only stock1 and we have holding then sell
        if stock1PriceMA > stock1Std and  strategySpecificArgs["SharesOwnedT1"] <= 0: 
            strategySpecificArgs["SharesOwnedT1"] -= 1
    #Enter Long Position: If Z<Lower Threshold, long the spread (buy underperforming asset, sell outperforming asset).
    if zScore<lowerBound:#stock2 is over performing or stock1 is underperforming
        # is stock2pricefrom last 20 point > 1 std deviation of only stock2 and we have holding then sell
        if stock2PriceMA > stock2Std and  strategySpecificArgs["SharesOwnedT2"] > 0:
            strategySpecificArgs["SharesOwnedT2"] -= 1
        # is stock1pricefrom last 20 point > 1 std deviation of only stock1 and we have holding then buy
        if stock1PriceMA > stock1Std and  strategySpecificArgs["SharesOwnedT1"] <= 0: 
            strategySpecificArgs["SharesOwnedT1"] += 1

    #Exit Position: If Z reverts to within the exit thresholds or approaches zero, close the position.

    # when the diffrenece between the stock falls sout of bouynds buy or sell 
    if newMovingAverage < lowerBound and strategySpecificArgs["SharesOwnedT1"] :
        return (strategySpecificArgs["movingAvgSeries"]) 

    return 1

# TODO consider removing ticker1 and ticker 2 as inputs since these were intended as string tickers, however since they are not needed maybe vestigial
# setup to inherit from data getter
class CoIntStdDivPair:
     def __init__(self, ticker1, ticker2 ):
        # Instance variables (unique to each object) 
        self.ticker1 = ticker1
        self.ticker2 = ticker2
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
            return (len(self.maSeriesS1, len(self.maSeriesS2)))

        # Gets  zScore, stdDiv, movingAvg for both stocks
        def getCoIntStdDivStats():
            return 1

        


# TODO Anuraj, returns zscore stddiv and moving avg
def CoIntStdDivStats() ->  Tuple[float, float, float]:
    return 1