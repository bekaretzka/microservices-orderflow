from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import engine, get_db
from app.schemas import ProductCreate, ProductRead
from app.models import Product, Base

@asynccontextmanager
async def lifespan(_: FastAPI):
    from app.models import Product

    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/products/", response_model=list[ProductRead])
def get_products(db: Session = Depends(get_db)):
    query = select(Product).order_by(Product.name)
    return list(db.scalars(query).all())

@app.get("/products/{product_id}", response_model=ProductRead)
def get_product(
    product_id: str,
    db: Session = Depends(get_db)
):
    product = db.get(Product, product_id)
    if product is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product

@app.post("/products/", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: Session = Depends(get_db)):
    product = Product(**payload.model_dump())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product
