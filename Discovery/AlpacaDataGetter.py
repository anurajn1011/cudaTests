from dateutil.relativedelta import relativedelta
import os
import pandas as pd
from datetime import date, datetime, timedelta
from alpaca_trade_api.rest import REST  # , TimeFrame, TimeFrameUnit
from alpaca.data.timeframe import TimeFrame, TimeFrameUnit
import json
import backtrader as bt
import backtrader.feeds as btfeeds
from alpaca.data import StockHistoricalDataClient, StockBarsRequest
from dotenv import load_dotenv

load_dotenv()

class AlpacaDataGetter:
    def __init__(self):
        """Initialize the Alpaca data client and load environment variables."""
        load_dotenv()
        self.api_key = os.getenv("ALPACA_KEY")
        self.secret_key = os.getenv("ALPACA_SECRET")

        if not self.api_key or not self.secret_key:
            raise EnvironmentError("Missing ALPACA_KEY or ALPACA_SECRET in environment variables.")

        self.stock_client = StockHistoricalDataClient(self.api_key, self.secret_key)

    def get_timeframe(self) -> TimeFrame:
        """Returns 1-minute timeframe object."""
        return TimeFrame(1, TimeFrameUnit("Min"))

    def string_to_datetime(self, date_str: str) -> datetime:
        """Convert date string to datetime object."""
        return datetime.strptime(date_str, "%Y-%m-%d")

    def get_symbol_history(self, symbol: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
        """Fetch historical bar data for a given symbol and date range."""
        request_params = StockBarsRequest(
            symbol_or_symbols=[symbol],
            timeframe=self.get_timeframe(),
            start=start_date,
            end=end_date,
        )
        bars = self.stock_client.get_stock_bars(request_params)
        return bars.df
"""
# Expected output format of get_symbol_history(symbol)
symbol  		timestamp                		open  	    high	    low 	    close	    volume		    trade_count	    vwap
BTC/USD 	    2022-09-01 05:00:00+00:00   	20049.0 	20285.0	    19555.0 	20160.0 	2396.3504   	18060.0		    19920.278135
        		2022-09-02 05:00:00+00:00   	20159.0 	20438.0 	19746.0 	19924.0 	1688.0641   	16730.0 		20045.987764
        		2022-09-03 05:00:00+00:00   	19924.0 	19963.0 	19661.0 	19802.0 	624.1013    	9853.0  		19794.111057
		        2022-09-04 05:00:00+00:00   	19801.0 	20060.0 	19599.0 	19892.0 	1361.6668   	8489.0  		19885.445568
		        2022-09-05 05:00:00+00:00   	19892.0 	20173.0 	19640.0 	19762.0 	2105.0539   	11900.0 		19814.853546
		        2022-09-06 05:00:00+00:00   	19763.0 	20025.0 	18539.0 	18720.0 	3291.1657   	19591.0 		19272.505607
		        2022-09-07 05:00:00+00:00   	18723.0 	19459.0 	18678.0 	19351.0 	2259.2351   	16204.0 		19123.487500
"""