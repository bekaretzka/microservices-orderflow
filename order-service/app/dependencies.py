
from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from api_clients.catalog_client import CatalogClient
from api_clients.payment_client import PaymentClient
from app.config import settings
from app.database import get_db
from app.service import OrderService

def get_catalog_client() -> CatalogClient:
    return CatalogClient(
        base_url=settings.catalog_service_url
    )

def get_payment_client() -> PaymentClient:
    return PaymentClient(
        base_url=settings.payment_service_url
    )

def get_order_service(
    db: Annotated[Session, Depends(get_db)],
    catalog_client: Annotated[CatalogClient, Depends(get_catalog_client)],
    payment_client: Annotated[PaymentClient, Depends(get_payment_client)]
) -> OrderService:
    return OrderService(session=db, catalog_client=catalog_client, payment_client=payment_client)