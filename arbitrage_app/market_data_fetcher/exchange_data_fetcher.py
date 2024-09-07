# exchange_data_fetcher.py
from arbitrage_app.market_data_fetcher.BinanceFetcher import BinanceFetcher
from arbitrage_app.market_data_fetcher.KrakenFetcher import KrakenFetcher


# from arbitrage_app.market_data_fetcher.NewExchangeFetcher import NewExchangeFetcher


class ExchangeDataFetcher:
    """
    Main class to manage the fetching of data from various exchanges.
    """

    def __init__(self):
        # Initialize fetcher instances for each supported exchange
        self.fetchers = {
            'binance': BinanceFetcher(),
            'kraken': KrakenFetcher(),
            # 'new_exchange': NewExchangeFetcher(),
        }

    async def fetch_data(self, exchange_id, symbol):
        """
        Fetch data for a specific symbol from the specified exchange asynchronously.

        Args:
            exchange_id (str): The ID of the exchange (e.g., 'binance', 'kraken', 'new_exchange').
            symbol (str): The trading pair symbol (e.g., 'BTC/USDT').

        Returns:
            dict: The fetched market data or None if fetching fails.
        """
        fetcher = self.fetchers.get(exchange_id)
        if not fetcher:
            print(f"No fetcher available for exchange: {exchange_id}")
            return None

        # Use the exchange-specific fetcher to get market data
        return await fetcher.fetch(symbol)

    async def close_all(self):
        """
        Close all exchange connections gracefully.
        """
        for fetcher in self.fetchers.values():
            await fetcher.close()
