"""
Products router

Endpoints to list products, add new ones and get the ones with broken links.

@author adrianpmdev
"""

from fastapi import APIRouter, status

from app import repository
from app.database import DbDep
from app.schemas import ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["Products"])


@router.get("", response_model=list[ProductRead])
def list_products(db: DbDep):
    """List every product with the result of its last check."""
    return repository.list_products(db)


@router.get("/broken", response_model=list[ProductRead])
def list_broken_products(db: DbDep):
    """List the products whose link was broken in the last check."""
    return repository.list_broken_products(db)


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(payload: ProductCreate, db: DbDep):
    """Add a product. Its link is checked in the next run."""
    return repository.create_product(db, payload.name, str(payload.url))
