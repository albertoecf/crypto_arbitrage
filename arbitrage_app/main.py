import asyncio
from arbitrage_app.market_data_fetcher.exchange_data_fetcher import ExchangeDataFetcher


async def main():
    # Initialize the ExchangeDataFetcher
    fetcher = ExchangeDataFetcher()

    # Fetch market data from various exchanges
    binance_data = await fetcher.fetch_data('binance', 'BTC/USDT')

    # Uncomment these lines to fetch data from Kraken and the new exchange
    # kraken_data = await fetcher.fetch_data('kraken', 'BTC/USD')
    # new_exchange_data = await fetcher.fetch_data('new_exchange', 'BTC/USDT')

    # Print the fetched data
    print("Binance Data:", binance_data)

    # Uncomment these lines to print the fetched data from Kraken and the new exchange
    # print("Kraken Data:", kraken_data)
    # print("New Exchange Data:", new_exchange_data)

    # Close all connections to exchanges
    await fetcher.close_all()


if __name__ == '__main__':
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())
    except Exception as e:
        print(f"Exception occurred: {e}")
    finally:
        loop.close()
