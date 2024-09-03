from aiokafka import AIOKafkaProducer
import json


async def init_producer():
    producer = AIOKafkaProducer(
        bootstrap_servers='localhost:9092',
        value_serializer=lambda v: json.dumps(v, default=str).encode('utf-8')  # Use default=str to handle datetime
    )
    await producer.start()
    return producer


async def produce_message(topic, message):
    """
    Produce messages to the specified Kafka topic.
    """
    producer = await init_producer()
    try:
        await producer.send_and_wait(topic, message)
        print(f"Message sent to topic {topic}: {message}")
    except Exception as e:
        print(f"Failed to send message to topic {topic}: {e}")
    finally:
        await producer.stop()
