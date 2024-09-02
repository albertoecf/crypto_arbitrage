import asyncio
from aiokafka import AIOKafkaConsumer
import json
from pathlib import Path

# Directory to store the JSON files
storage_dir = Path('./market_data')

# Create storage directory if it doesn't exist
storage_dir.mkdir(exist_ok=True)


async def consume_messages():
    consumer = AIOKafkaConsumer(
        'market-data-topic',
        bootstrap_servers='localhost:9092',
        group_id='market-data-group',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    await consumer.start()
    try:
        print("Listening for market data messages...")
        async for message in consumer:
            market_data = message.value
            print(f"Received market data: {market_data}")
            await store_message_in_file(market_data)
    finally:
        await consumer.stop()


async def store_message_in_file(market_data):
    """Store the market data in a JSON file based on the symbol."""
    symbol = market_data['symbol'].replace('/', '_')  # Replace '/' in symbol with '_' for valid filenames
    file_path = storage_dir / f"{symbol}.json"

    # Read existing data from the file
    if file_path.exists():
        with open(file_path, 'r') as file:
            try:
                existing_data = json.load(file)
            except json.JSONDecodeError:
                existing_data = []  # If the file is empty or corrupt, start fresh
    else:
        existing_data = []

    # Append the new market data
    existing_data.append(market_data)

    # Write the updated data back to the file
    with open(file_path, 'w') as file:
        json.dump(existing_data, file, indent=4)


if __name__ == "__main__":
    asyncio.run(consume_messages())
