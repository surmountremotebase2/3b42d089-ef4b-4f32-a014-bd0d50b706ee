from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import RSI, MACD
from surmount.logging import log
from surmount.data import SocialSentiment

class TradingStrategy(Strategy):
    def __init__(self):
        # Define a list of tech stock tickers to trade
        self.tickers = ["AAPL", "MSFT", "GOOGL", "FB", "AMZN"]
        # Adding SocialSentiment to the data_list for each ticker
        self.data_list = [SocialSentiment(ticker) for ticker in self.tickers]

    @property
    def interval(self):
        # Use daily data for this strategy
        return "1day"

    @property
    def assets(self):
        # Return the assets this strategy is interested in
        return self.tickers

    @property
    def data(self):
        return self.data_list

    def run(self, data):
        allocation_dict = {}
        for ticker in self.tickers:
            # Initialize allocation to 0
            allocation_dict[ticker] = 0
            ohlcv_data = data["ohlcv"]

            # Calculate RSI and MACD for each ticker
            rsi = RSI(ticker=ticker, data=ohlcv_data, length=14)
            macd = MACD(ticker=ticker, data=ohlcv_data, fast=12, slow=26)
            
            # Retrieve the latest social sentiment for the ticker
            sentiment = data[("social_sentiment", ticker)]

            if len(sentiment) > 0:
                # Check the latest sentiment score
                latest_sentiment = sentiment[-1]['twitterSentiment']
                
                # Buy signal: RSI below 70 (to avoid overbought conditions), MACD line above the signal line, and positive social sentiment
                if rsi[-1] < 70 and macd["MACD"][-1] > macd["signal"][-1] and latest_sentiment > 0.5:
                    allocation_dict[ticker] = 0.2  # Allocate 20% of the portfolio to this stock
                    
                # Log the decision making for debugging or future analysis
                log(f"Allocating {allocation_dict[ticker]*100}% to {ticker} based on RSI, MACD, and social sentiment.")

        # Normalize the allocations to ensure they sum up to 1 or less
        total_allocation = sum(allocation_dict.values())
        if total_allocation > 1:
            allocation_dict = {ticker: allocation/total_allocation for ticker, allocation in allocation_dict.items()}
        
        return TargetAllocation(allocation_dict)