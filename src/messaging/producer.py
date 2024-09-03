import asyncio
import ccxt.async_support as ccxt
import yaml
from pathlib import Path
import datetime
from aiokafka import AIOKafkaProducer
import json
from src.settings import BINANCE_API_KEY, BINANCE_SECRET, KRAKEN_API_KEY, KRAKEN_SECRET

# Load configuration files
base_dir = Path(__file__).resolve().parent.parent
config_dir = base_dir / 'config'

with open(config_dir / 'exchanges_config.yaml', 'r') as file:
    exchange_config = yaml.safe_load(file)

# Mapping of exchange credentials
exchange_credentials = {
    'binance': {'api_key': BINANCE_API_KEY, 'secret': BINANCE_SECRET},
    'kraken': {'api_key': KRAKEN_API_KEY, 'secret': KRAKEN_SECRET},
}


async def fetch_market_data(exchange_id, symbol):
    """Fetch market data from the exchange."""
    try:
        async with getattr(ccxt, exchange_id)({
            'apiKey': exchange_credentials[exchange_id]['api_key'],
            'secret': exchange_credentials[exchange_id]['secret'],
            'enableRateLimit': True
        }) as exchange:
            ticker = await exchange.fetch_ticker(symbol)
            data = {
                'exchange': exchange_id,
                'symbol': symbol,
                'price': ticker['last'],
                'bid': ticker['bid'],
                'ask': ticker['ask'],
                'timestamp': datetime.datetime.utcfromtimestamp(ticker['timestamp'] / 1000).isoformat() if ticker[
                    'timestamp'] else 'N/A'
            }
            print(data)
            return data
    except Exception as e:
        print(f"Error fetching data from {exchange_id}: {e}")
        return None


async def produce_messages(producer):
    """Produce messages to Kafka."""
    tasks = []

    for exchange_id, config in exchange_config.items():
        for symbol in config['symbols']:
            tasks.append(fetch_market_data(exchange_id, symbol))

    market_data_list = await asyncio.gather(*tasks)

    for market_data in market_data_list:
        if market_data:
            await producer.send_and_wait('market-data-topic', json.dumps(market_data).encode('utf-8'))


async def main():
    producer = AIOKafkaProducer(bootstrap_servers='localhost:9092')
    await producer.start()
    try:
        await produce_messages(producer)
    finally:
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(main())
