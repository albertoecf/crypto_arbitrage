import asyncio
from aiokafka import AIOKafkaProducer
import json


async def send_one_message(producer, topic, message):
    """Send a single message to the Kafka topic."""
    try:
        print(f"Publishing message: {message}")
        await producer.send_and_wait(topic, json.dumps(message).encode('utf-8'))
    except Exception as e:
        print(f"Failed to send message: {e}")


async def produce_messages():
    # Initialize Kafka producer
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092'
    )

    # Start the producer
    await producer.start()
    try:
        # Define the topic and messages
        topic = 'test-topic'
        messages = [
            {"message": "Hello Kafka!"},
            {"message": "Kafka is great!"},
            {"message": "Python and Kafka are working together!"}
        ]

        # Send messages to the Kafka topic
        for message in messages:
            await send_one_message(producer, topic, message)
            await asyncio.sleep(1)  # Sleep for a second between messages for demo purposes
    finally:
        # Stop the producer
        await producer.stop()


if __name__ == "__main__":
    asyncio.run(produce_messages())
