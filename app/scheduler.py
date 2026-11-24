"""
Scheduler

Background task that runs the link check periodically while the API is up.
The blocking HTTP work runs in a thread so it never blocks the event loop.

@author adrianpmdev
"""

import asyncio
import logging

from app.checker import CheckAlreadyRunningError, check_all_products
from app.config import CHECK_INTERVAL_MINUTES

logger = logging.getLogger(__name__)


async def run_periodic_checks() -> None:
    while True:
        try:
            await asyncio.to_thread(check_all_products)
        except CheckAlreadyRunningError:
            logger.info("Skipping scheduled check: another check is still running")
        except Exception:  # Keep the loop alive whatever happens in one run.
            logger.exception("Periodic link check failed")
        await asyncio.sleep(CHECK_INTERVAL_MINUTES * 60)
