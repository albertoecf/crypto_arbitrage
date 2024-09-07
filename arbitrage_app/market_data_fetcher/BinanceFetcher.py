from arbitrage_app.market_data_fetcher.BaseFetcher import BaseFetcher
from arbitrage_app.settings import BINANCE_API_KEY, BINANCE_SECRET


class BinanceFetcher(BaseFetcher):
    """
    Fetches market data from Binance exchange using ccxt.
    """

    def __init__(self):
        # Use credentials from settings
        super().__init__(
            exchange_id='binance',
            api_key=BINANCE_API_KEY,
            secret=BINANCE_SECRET
        )
