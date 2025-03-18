from surmount.base_class import Strategy, TargetAllocation
from surmount.data import Asset

class TradingStrategy(Strategy):
    def __init__(self):
        # Specify a list of tickers you're interested in.
        self.tickers = ["AAPL", "MSFT", "T", "VZ", "IBM", "KO", "PEP", "MO"]

        # Create Asset objects for each ticker to access financial metrics
        self.data_list = [Asset(i) for i in self.tickers]

    @property
    def interval(self):
        # Define the preferred interval for data refresh
        return "1day"

    @property
    def assets(self):
        # Define which assets this strategy targets
        return self.tickers

    @property
    def data(self):
        # Provide access to the required data for each asset
        return self.data_list

    def run(self, data):
        # Initialize an empty dictionary for target allocations
        allocation_dict = {}

        # Loop through each asset and their data
        for asset in self.data_list:
            ticker = asset.ticker
            
            # Here, we'making a hypothetical call to Asset object assuming it can return 
            # dividend_yield and pe_ratio which is not a standard part of Surmount's API 
            # based on the provided examples. This is for demonstration purposes.
            dividend_yield = data[asset].dividend_yield
            pe_ratio = data[asset].pe_ratio
            
            # Check if the dividend yield is above 5% and the P/E ratio is below 15x
            if dividend_yield > 5 and pe_ratio < 15:
                allocation_dict[ticker] = 1  # Placeholder for eligible assets

        # Calculate equal weighting for eligible assets
        eligible_assets_count = len(allocation_dict)
        if eligible_assets_count > 0:
            equal_weight = 1.0 / eligible_assets_count
            for ticker in allocation_dict.keys():
                allocation_dict[ticker] = equal_weight
        else:
            # If no assets meet the criteria, return an empty allocation
            return TargetAllocation({})

        return TargetAllocation(allocation_dict)