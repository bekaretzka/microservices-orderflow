import json

import aio_pika
from aio_pika.abc import AbstractRobustConnection, AbstractIncomingMessage, AbstractConnection

from app.config import settings
from app.database import SessionLocal
from app.models import Notification

async def connect_rabbitmq() -> AbstractRobustConnection:
    return await aio_pika.connect_robust(settings.rabbitmq_url)

async def handle_payment_events(message: AbstractIncomingMessage):
    async with message.process():
        event = json.loads(message.body.decode("utf-8"))

        with SessionLocal() as session:
            notification = Notification(
                order_id = event["order_id"],
                message=(
                    f"Заказ {event['order_id']} успешно оплачен. "
                    f"Сумма: {event['amount']}"
                )
            )
            session.add(notification)
            session.commit()

async def start_payments_consume(connection: AbstractConnection):
    channel = await connection.channel()
    payment_exchange = await channel.declare_exchange(settings.payment_exchange_name)
    notification_queue = await channel.declare_queue(settings.notification_queue_name)

    await notification_queue.bind(payment_exchange, routing_key=settings.payment_succeeded_routing_key)
    await notification_queue.consume(handle_payment_events)