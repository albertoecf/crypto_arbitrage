# Market Data Fetcher to fetch data from exchanges

import asyncio
import ccxt.async_support as ccxt
import yaml
from pathlib import Path
import datetime
import src.settings as settings
from src.utils.message_translator import translate_message
from src.messaging.producer import produce_message

base_dir = Path(__file__).resolve().parent.parent
config_dir = base_dir / 'config'
exchange_dir = config_dir / 'exchanges_config.yaml'

with open(exchange_dir, 'r') as file:
    exchange_config = yaml.safe_load(file)

exchange_credentials = {
    'binance': {'api_key': settings.BINANCE_API_KEY, 'secret': settings.BINANCE_SECRET},
    'kraken': {'api_key': settings.KRAKEN_API_KEY, 'secret': settings.KRAKEN_SECRET},
}


async def fetch_market_data(exchange_id, symbol):
    try:
        async with getattr(ccxt, exchange_id)(
                {
                    'apiKey': exchange_credentials[exchange_id]['api_key'],
                    'secret': exchange_credentials[exchange_id]['secret'],
                    'enableRateLimit': True,
                }
        ) as exchange:
            raw_data = await exchange.fetch_ticker(symbol)

            raw_message = {
                'exchange': exchange_id,
                'symbol': symbol,
                'data': raw_data,
            }

            translated_message = translate_message(raw_message)

            if translated_message:
                await produce_message('NEW_TRADING_PAIR', translated_message)
                print(f"Produced message for {exchange_id} {symbol}: {translated_message}")
            else:
                print(f"Failed to translate message for {exchange_id} {symbol}")

    except Exception as e:
        print(f"Error fetching data from {exchange_id}: {e}")


async def main():
    tasks = []

    for exchange_id, config in exchange_config.items():
        for symbol in config['symbols']:
            tasks.append(fetch_market_data(exchange_id, symbol))

    await asyncio.gather(*tasks)


if __name__ == '__main__':
    asyncio.run(main())
