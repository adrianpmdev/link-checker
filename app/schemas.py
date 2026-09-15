"""
Schemas

Pydantic models used to validate requests and shape API responses.

@author adrianpmdev
"""

from datetime import datetime

from pydantic import BaseModel, Field, HttpUrl


class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    url: HttpUrl


class ProductRead(BaseModel):
    id: int
    name: str
    url: str
    status_code: int | None
    is_broken: bool
    last_checked_at: datetime | None


class CheckSummary(BaseModel):
    checked: int
    broken: int
