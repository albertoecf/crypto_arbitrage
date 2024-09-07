import ccxt.async_support as ccxt


class BaseFetcher:
    """
    Base class for fetching market data from various exchanges.
    """

    def __init__(self, exchange_id, api_key, secret):
        """
        Initializes the fetcher with the exchange details.

        Args:
            exchange_id (str): The ID of the exchange (e.g., 'binance', 'kraken').
            api_key (str): API key for the exchange.
            secret (str): Secret key for the exchange.
        """
        self.exchange_id = exchange_id
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': api_key,
            'secret': secret,
            'enableRateLimit': True
        })

    async def fetch(self, symbol):
        """
        Fetches market data for the specified symbol from the exchange.

        Args:
            symbol (str): The trading pair symbol (e.g., 'BTC/USDT').

        Returns:
            dict: The fetched market data or None if fetching fails.
        """
        try:
            ticker = await self.exchange.fetch_ticker(symbol)
            await self.exchange.close()
            return ticker
        except Exception as e:
            print(f"Error fetching data from {self.exchange_id}: {e}")
            return None

    async def close(self):
        """
        Closes the exchange connection gracefully.
        """
        await self.exchange.close()
