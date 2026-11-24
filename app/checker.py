"""
Checker

Link verification logic. A link is considered broken when the request fails
or the server answers with a 4xx/5xx status code. A lock prevents two
checks from running at the same time.

@author adrianpmdev
"""

import logging
import threading

import requests

from app import repository
from app.config import REQUEST_TIMEOUT_SECONDS, USER_AGENT
from app.database import get_connection

logger = logging.getLogger(__name__)

HEADERS = {"User-Agent": USER_AGENT}

_run_lock = threading.Lock()


class CheckAlreadyRunningError(Exception):
    """Raised when a check is requested while another one is still running."""


def check_url(url: str) -> tuple[int | None, bool]:
    """Returns (status_code, is_broken). status_code is None if unreachable."""
    try:
        response = requests.head(
            url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SECONDS, allow_redirects=True
        )
        # Some servers do not support HEAD, so retry with GET.
        if response.status_code in (403, 405):
            response = requests.get(
                url, headers=HEADERS, timeout=REQUEST_TIMEOUT_SECONDS, allow_redirects=True
            )
    except requests.RequestException as error:
        logger.info("Unreachable link %s: %s", url, error)
        return None, True

    return response.status_code, response.status_code >= 400


def check_all_products() -> dict:
    """Checks every product link and stores the result. Returns a summary.

    Raises CheckAlreadyRunningError if another check is still running.
    """
    if not _run_lock.acquire(blocking=False):
        raise CheckAlreadyRunningError
    try:
        return _check_and_save_all()
    finally:
        _run_lock.release()


def _check_and_save_all() -> dict:
    connection = get_connection()
    try:
        products = repository.list_products(connection)
        broken = 0
        for product in products:
            status_code, is_broken = check_url(product["url"])
            repository.save_check_result(connection, product["id"], status_code, is_broken)
            broken += int(is_broken)
    finally:
        connection.close()

    logger.info("Checked %d links, %d broken", len(products), broken)
    return {"checked": len(products), "broken": broken}
