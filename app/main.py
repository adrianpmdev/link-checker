"""
Main

FastAPI application entry point. Initializes the database, starts the
periodic link check and registers the routers.

@author adrianpmdev
"""

import asyncio
import contextlib
import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import init_db
from app.routers import checks, products
from app.scheduler import run_periodic_checks

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    task = asyncio.create_task(run_periodic_checks())
    yield
    task.cancel()
    with contextlib.suppress(asyncio.CancelledError):
        await task


app = FastAPI(
    title="Link Checker",
    description="Internal service that periodically checks that product links still work.",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(products.router)
app.include_router(checks.router)


@app.get("/", tags=["Health"])
def health():
    return {"status": "ok"}
