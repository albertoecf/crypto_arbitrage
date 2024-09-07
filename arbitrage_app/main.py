import asyncio
from arbitrage_app.market_data_fetcher.exchange_data_fetcher import ExchangeDataFetcher


async def main():
    # Initialize the ExchangeDataFetcher
    fetcher = ExchangeDataFetcher()

    # Fetch market data from various exchanges and their trading pairs
    market_data = await fetcher.fetch_data()

    # Print the fetched data
    for exchange, data in market_data.items():
        print(f"Data for {exchange}:")
        for symbol, info in data.items():
            print(f"  {symbol}: {info}")

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
