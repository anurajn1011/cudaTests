from DataProcessing import DataProcessing
# dates

def backtest(algoName,algo, ticker1, ticker2, startDate, endDate,initialValue) :
    """Run a backtest given market data and trading signals. Returns a df with following columns"""
    # columns algoName, ticker1, ticker2, startDate, endDate,initialValue, finalValue, percent change
    results = []
    for price in data:
        signal = strategy_func(price, *strategy_args)
        results.append((price, signal))
    return results
    pass

def CoIntStdDiv():
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