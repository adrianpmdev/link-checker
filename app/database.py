"""
Database

SQLite connection handling, schema creation and sample data seeding.

@author adrianpmdev
"""

import sqlite3
from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends

from app import config

SCHEMA = """
CREATE TABLE IF NOT EXISTS products (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT    NOT NULL,
    url             TEXT    NOT NULL,
    status_code     INTEGER,
    is_broken       INTEGER NOT NULL DEFAULT 0,
    last_checked_at TEXT
);
"""

SAMPLE_PRODUCTS = [
    ("Wireless headphones", "https://www.python.org"),
    ("Mechanical keyboard", "https://example.com"),
    ("Gaming mouse", "https://github.com"),
    ("USB-C hub", "https://example.com/this-page-does-not-exist"),
    ("Webcam HD", "https://this-domain-does-not-exist.invalid"),
]


def get_connection() -> sqlite3.Connection:
    """Opens a new SQLite connection that returns rows as dict-like objects."""
    config.DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    connection = sqlite3.connect(config.DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def get_db() -> Iterator[sqlite3.Connection]:
    """FastAPI dependency: one connection per request, always closed."""
    connection = get_connection()
    try:
        yield connection
    finally:
        connection.close()


DbDep = Annotated[sqlite3.Connection, Depends(get_db)]


def init_db() -> None:
    """Creates the schema and, if enabled, inserts sample products when the table is empty."""
    connection = get_connection()
    try:
        connection.executescript(SCHEMA)
        if not config.SEED_SAMPLE_DATA:
            return
        count = connection.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if count == 0:
            connection.executemany(
                "INSERT INTO products (name, url) VALUES (?, ?)", SAMPLE_PRODUCTS
            )
            connection.commit()
    finally:
        connection.close()
