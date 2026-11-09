import json

from aiokafka import AIOKafkaConsumer, ConsumerRecord
from pymongo.collection import Collection

from app.config import settings


async def save_event(collection: Collection, message: ConsumerRecord):
    event = json.loads(message.value)
    await collection.insert_one(event)


async def consume_evenets(collection: Collection):
    consumer = AIOKafkaConsumer(
        settings.kafka_topic, 
        bootstrap_servers=settings.kafka_bootstrap_server
    )

    await consumer.start()

    try:
        async for message in consumer:
            await save_event(collection, message)
    finally:
        await consumer.stop()