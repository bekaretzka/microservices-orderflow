from fastapi import FastAPI, Depends, HTTPException, status
from contextlib import asynccontextmanager

from app.database import engine
from app.schemas import OrderCreateSchema, OrderReadSchema
from app.models import Base
from app.service import OrderService
from app.dependencies import get_order_service
from app.rabbitmq import connect_rabbitmq, start_payments_consume
from app.config import NotFoundError

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


@app.get("/orders/{order_id}", response_model=OrderReadSchema)
def get_order(
    order_id,
    order_service: OrderService = Depends(get_order_service)
): 
    try:
        return order_service.get(order_id)
    except NotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order Not Found"
        )

@app.get("/orders", response_model=list[OrderReadSchema])
def get_orders(
    order_service: OrderService = Depends(get_order_service)
): 
    return order_service.get_all()

@app.post("/orders/", response_model=OrderReadSchema)
def create_order(
    payload: OrderCreateSchema,
    order_service: OrderService = Depends(get_order_service)
):
    return order_service.create(payload)
