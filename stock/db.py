"""数据库连接与建表。"""

import os
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


def db_path() -> str:
    return os.environ.get("STOCK_DB", str(BASE_DIR / "stock.db"))


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(db_path(), timeout=0.2, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    conn = connect()
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS stock (
                sku TEXT PRIMARY KEY,
                qty INTEGER NOT NULL
            );

            CREATE TABLE IF NOT EXISTS orders (
                order_id TEXT NOT NULL,
                sku TEXT NOT NULL,
                qty INTEGER NOT NULL
            );
            """
        )
    finally:
        conn.close()


def reset(initial: dict[str, int]) -> None:
    conn = connect()
    try:
        conn.execute("DELETE FROM stock")
        conn.execute("DELETE FROM orders")
        for sku, qty in initial.items():
            conn.execute("INSERT INTO stock (sku, qty) VALUES (?, ?)", (sku, qty))
    finally:
        conn.close()
