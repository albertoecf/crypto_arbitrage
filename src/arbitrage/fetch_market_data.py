import asyncio
import ccxt.async_support as ccxt  # Use the async support version of ccxt
import yaml
from pathlib import Path
import datetime
from src.settings import BINANCE_API_KEY, BINANCE_SECRET

# Load configuration files
base_dir = Path(__file__).resolve().parent.parent
config_dir = base_dir / 'config'

with open(config_dir / 'exchanges_config.yaml', 'r') as file:
    exchange_config = yaml.safe_load(file)

# Mapping of exchange credentials
exchange_credentials = {
    'binance': {'api_key': BINANCE_API_KEY, 'secret': BINANCE_SECRET},
    # Add more exchange credentials here if needed
}


async def fetch_market_data(exchange_id, symbol):
    try:
        # Initialize the exchange with API credentials from settings
        async with getattr(ccxt, exchange_id)({
            'apiKey': exchange_credentials[exchange_id]['api_key'],
            'secret': exchange_credentials[exchange_id]['secret'],
            'enableRateLimit': True
        }) as exchange:

            # Fetch the ticker data for the specified symbol asynchronously
            ticker = await exchange.fetch_ticker(symbol)

            # Create a formatted data structure
            data = {
                'exchange': exchange_id,
                'symbol': symbol,
                'price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'timestamp': datetime.datetime.utcfromtimestamp(ticker['timestamp'] / 1000).isoformat() if ticker[
                    'timestamp'] else 'N/A'
            }

            # Print the data to the console for testing
            print(data)
            return data

    except Exception as e:
        print(f"Error fetching data from {exchange_id}: {e}")


async def main():
    tasks = []

    # Iterate over the exchanges in the configuration file
    for exchange_id, config in exchange_config.items():
        # Iterate over each trading pair (symbol) for the given exchange
        for symbol in config['symbols']:
            tasks.append(fetch_market_data(exchange_id, symbol))

    # Run all tasks concurrently
    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
