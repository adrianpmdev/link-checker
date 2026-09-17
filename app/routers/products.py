"""
Products router

Endpoints to list products, add new ones and get the ones with broken links.

@author adrianpmdev
"""

import sqlite3

from fastapi import APIRouter, Depends, status

from app import repository
from app.database import get_db
from app.schemas import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductRead])
def list_products(db: sqlite3.Connection = Depends(get_db)):
    return repository.list_products(db)


@router.get("/broken", response_model=list[ProductRead])
def list_broken_products(db: sqlite3.Connection = Depends(get_db)):
    return repository.list_broken_products(db)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: sqlite3.Connection = Depends(get_db)):
    return repository.create_product(db, payload.name, str(payload.url))
