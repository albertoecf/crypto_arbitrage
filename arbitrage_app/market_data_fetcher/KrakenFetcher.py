from arbitrage_app.market_data_fetcher.BaseFetcher import BaseFetcher
from arbitrage_app.settings import KRAKEN_API_KEY, KRAKEN_SECRET


class KrakenFetcher(BaseFetcher):
    """
    Fetches market data from Kraken exchange using ccxt.
    """

    def __init__(self):
        super().__init__(
            exchange_id='kraken',
            api_key=KRAKEN_API_KEY,
            secret=KRAKEN_SECRET
        )
