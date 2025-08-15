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
# TODO Need to redesigning the return tuple into a dictionary this was various key values can be easily accessed and return uniformly in the back test function incase data is needed on a recurring basis
def CoIntStdDiv(newData, strategySpecificArgs):

    strategySpecificArgs["movingAvgSeries"].appened(newData)
    if len(strategySpecificArgs["movingAvgSeries"]) < 1200:
        movingAvgSeriesSum = sum(strategySpecificArgs["movingAvgSeries"])
        movingAvgSeriesLen = len(strategySpecificArgs["movingAvgSeries"])
        newMovingAverage  =  movingAvgSeriesSum/movingAvgSeriesLen
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
    # Signal Generation-------------------------------------
    
    #Enter Short Position: If Z>Upper Threshold, short the spread (sell outperforming asset, buy underperforming asset).
    if zScore>upperBound: # is opposite
        pass
    #Enter Long Position: If Z<Lower Threshold, long the spread (buy underperforming asset, sell outperforming asset).
    if zScore<lowerBound:#stock2 is over performing or stock1 is underperforming
        if 1 > 1 # is stock2pricefrom last 20 point > 1 std deviation of only stock2 and we have holding then sell
            pass
        if 1 > 1 # is stock1pricefrom last 20 point > 1 std deviation of only stock1 and we have holding then buy
            pass 

    #Exit Position: If Z reverts to within the exit thresholds or approaches zero, close the position.

    # when the diffrenece between the stock falls sout of bouynds buy or sell 
    if newMovingAverage < lowerBound and strategySpecificArgs["SharesOwnedT1"] :
        return (strategySpecificArgs["movingAvgSeries"]) 

    return 1

# setup to inherit from data getter
class Pair:



# TODO Anuraj, returns zscore stddiv and moving avg
def CoIntStdDivStats() ->  Tuple[float, float, float]:
    return 1