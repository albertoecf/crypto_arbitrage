# exchange_data_fetcher.py

from arbitrage_app.market_data_fetcher.BinanceFetcher import BinanceFetcher
from arbitrage_app.market_data_fetcher.KrakenFetcher import KrakenFetcher
from arbitrage_app.utils.config_reader import load_exchange_config


class ExchangeDataFetcher:
    """
    Main class to manage the fetching of data from various exchanges.
    """

    def __init__(self):
        # Load exchanges and their symbols from configuration file
        self.exchange_config = load_exchange_config()

        # Initialize fetcher instances for each supported exchange
        self.fetchers = {
            'binance': BinanceFetcher(),
            'kraken': KrakenFetcher(),
            # Add more fetchers here as needed
        }

    async def fetch_data(self):
        """
        Fetch data for all exchanges and their trading pairs asynchronously.

        Returns:
            dict: A dictionary with exchange names as keys and their market data as values.
        """
        results = {}

        for exchange_id, config in self.exchange_config.items():
            fetcher = self.fetchers.get(exchange_id)
            if not fetcher:
                print(f"No fetcher available for exchange: {exchange_id}")
                continue

            # Fetch data for each trading pair
            results[exchange_id] = {}
            for symbol in config['symbols']:
                results[exchange_id][symbol] = await fetcher.fetch(symbol)

        return results

    async def close_all(self):
        """
        Close all exchange connections gracefully.
        """
        for fetcher in self.fetchers.values():
            await fetcher.close()
