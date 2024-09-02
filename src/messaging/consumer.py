import asyncio
from aiokafka import AIOKafkaConsumer
import json


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
    finally:
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_messages())
