from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends

from app.database import engine
from app.models import Base
from app.rabbitmq import connect_rabbitmq, start_payments_consume
from app.schemas import NotificationReadSchema
from app.service import NotificationService
from app.dependencies import get_notification_service


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)

    connection = await connect_rabbitmq()
    await start_payments_consume(connection=connection)

    try:
        yield
    finally:
        await connection.close()

app = FastAPI(lifespan=lifespan)

@app.get("/notifications/{notification_id}", response_model=NotificationReadSchema)
def get_notification(
    notification_id: str,
    notification_service: NotificationService = Depends(get_notification_service)
):
    return notification_service.get(notification_id)

@app.get("/notifications", response_model=list[NotificationReadSchema])
def get_notification(
    notification_service: NotificationService = Depends(get_notification_service)
):
    return notification_service.get_all()

@app.get("/health")
def health():
    return {"status": "ok"}