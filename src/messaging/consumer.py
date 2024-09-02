import asyncio
from aiokafka import AIOKafkaConsumer
import json


async def consume_messages():
    # Initialize Kafka consumer
    consumer = AIOKafkaConsumer(
        'test-topic',
        bootstrap_servers='localhost:9092',
        group_id='my-group',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )

    # Start the consumer
    await consumer.start()
    try:
        print("Listening for messages...")
        async for message in consumer:
            print(f"Received message: {message.value}")
    finally:
        # Stop the consumer
        await consumer.stop()


if __name__ == "__main__":
    asyncio.run(consume_messages())
