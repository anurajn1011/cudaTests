from DataProcessing import DataProcessing
import statistics
# dates

def backtest(algoName,algo, tickers, startDate, endDate,initialValue) :
    """Run a backtest given market data and trading signals. Returns a df with following columns"""
    # columns algoName, ticker1, ticker2, startDate, endDate,initialValue, finalValue, percent change
    results = []
    for price in data:
        signal = strategy_func(price, *strategy_args)
        results.append((price, signal))
    return results
    pass
# TODO consider adding moving average class from crossover moving average trading algo
# TODO Need to redesigning the return tuple into a dictionary this was various key values can be easily accessed and return uniformly in the back test function incase data is needed on a recurring basis
def CoIntStdDiv(ticker1NewData, ticker2NewData, movingAvgSeries, movingAvgVal, newData ):

    movingAvgSeries.appened(newData)
    if len(movingAvgSeries) < 1200:
        movingAvgSeriesSum = sum(movingAvgSeries)
        movingAvgSeriesLen = len(movingAvgSeries)
        newMovingAverage  =  movingAvgSeriesSum/movingAvgSeriesLen
        return (movingAvgSeries, newMovingAverage, "No Change")
    # take a moving avg over 1200 steps (20 min) 
    movingAvgSeries.pop(0)
    
    # recalculate new moving avg
    movingAvgSeriesSum = sum(movingAvgSeries)
    movingAvgSeriesLen = len(movingAvgSeries)
    newMovingAverage  =  movingAvgSeriesSum/movingAvgSeriesLen
    # take stdiv of the moving avg
    std_dev = statistics.stdev(movingAvgSeries)
    # set upper bound to stdiv + moving avg 
    upperBound = std_dev + newMovingAverage
    # set lower bound to stdiv - moving avg 
    lowerBound = std_dev - newMovingAverage
    # when the diffrenece between the stock falls sout of bouynds buy or sell 
    if newMovingAverage < lowerBound and :
        return (movingAvgSeries, newMovingAverage, "Buy")

    return 1






# This kind of nesting is the goal to facilitate good UX
# def algo1(price, param_a, param_b):
#     """Decide buy/sell/hold based on current price and params."""
#     if price > param_a:
#         return "BUY"
#     elif price < param_b:
#         return "SELL"
#     return "HOLD"

# def backtest(strategy_func, data, *strategy_args):
#     """Run backtest by calling strategy_func on each price."""
#     results = []
#     for price in data:
#         signal = strategy_func(price, *strategy_args)
#         results.append((price, signal))
#     return results

# # Example market data
# prices = [95, 102, 88, 110, 97]

# # Pass the function itself, plus its params
# results = backtest(algo1, prices, 100, 90)

# for price, signal in results:
#     print(f"Price: {price}, Signal: {signal}")