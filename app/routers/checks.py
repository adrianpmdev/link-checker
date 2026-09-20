"""
Checks router

Endpoint to run a link check on demand, without waiting for the scheduler.

@author adrianpmdev
"""

from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool

from app.checker import check_all_products
from app.schemas import CheckSummary

router = APIRouter(prefix="/checks", tags=["Checks"])


@router.post("/run", response_model=CheckSummary)
async def run_check():
    return await run_in_threadpool(check_all_products)
