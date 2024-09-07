# exchange_data_fetcher.py

from arbitrage_app.utils.config_reader import load_exchange_config
import importlib


class ExchangeDataFetcher:
    """
    Main class to manage the fetching of data from various exchanges.
    """

    def __init__(self):
        # Load exchanges and their symbols from the configuration file
        self.exchange_config = load_exchange_config()

        # Initialize fetcher instances for each supported exchange dynamically
        self.fetchers = {}
        for exchange_id, config in self.exchange_config.items():
            fetcher_class_name = config.get('exchange_class')
            if fetcher_class_name:
                # Dynamically load the fetcher class based on the config
                fetcher_class = self._get_fetcher_class(fetcher_class_name)
                if fetcher_class:
                    self.fetchers[exchange_id] = fetcher_class()

    def _get_fetcher_class(self, class_name):
        """
        Dynamically loads a fetcher class based on its name.

        Args:
            class_name (str): Name of the fetcher class.

        Returns:
            class: The fetcher class or None if not found.
        """
        try:
            # Dynamically import the module containing the fetcher class
            module_name = f'arbitrage_app.market_data_fetcher.{class_name}'
            module = importlib.import_module(module_name)
            return getattr(module, class_name)
        except (ImportError, AttributeError) as e:
            print(f"Error loading fetcher class '{class_name}': {e}")
            return None

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
