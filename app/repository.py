"""
Repository

Data access layer for products. Keeps every SQL query in one place.

@author adrianpmdev
"""

import sqlite3
from datetime import datetime, timezone


def _to_dict(row: sqlite3.Row) -> dict:
    product = dict(row)
    product["is_broken"] = bool(product["is_broken"])
    return product


def list_products(connection: sqlite3.Connection) -> list[dict]:
    rows = connection.execute("SELECT * FROM products ORDER BY id").fetchall()
    return [_to_dict(row) for row in rows]


def list_broken_products(connection: sqlite3.Connection) -> list[dict]:
    rows = connection.execute(
        "SELECT * FROM products WHERE is_broken = 1 ORDER BY id"
    ).fetchall()
    return [_to_dict(row) for row in rows]


def create_product(connection: sqlite3.Connection, name: str, url: str) -> dict:
    cursor = connection.execute(
        "INSERT INTO products (name, url) VALUES (?, ?)", (name, url)
    )
    connection.commit()
    row = connection.execute(
        "SELECT * FROM products WHERE id = ?", (cursor.lastrowid,)
    ).fetchone()
    return _to_dict(row)


def save_check_result(
    connection: sqlite3.Connection,
    product_id: int,
    status_code: int | None,
    is_broken: bool,
) -> None:
    connection.execute(
        """
        UPDATE products
        SET status_code = ?, is_broken = ?, last_checked_at = ?
        WHERE id = ?
        """,
        (
            status_code,
            int(is_broken),
            datetime.now(timezone.utc).isoformat(),
            product_id,
        ),
    )
    connection.commit()
