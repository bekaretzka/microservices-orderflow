from typing import Any
from fastapi import APIRouter, status

from app.api_client import request_service
from app.config import settings
from app.schemas import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])

@router.get("")
async def get_products() -> Any:
    return await request_service("GET", f"{settings.CATALOG_SERVICE_URL}/products/")

@router.get("/{product_id}")
async def get_product(product_id: str) -> Any:
    return await request_service("GET", f"{settings.CATALOG_SERVICE_URL}/products/{product_id}")

@router.post("", status_code=status.HTTP_201_CREATED)
async def create_product(payload: ProductCreate) -> ProductRead:
    return await request_service("POST", f"{settings.CATALOG_SERVICE_URL}/products/", json_body=payload.model_dump(mode="json"))