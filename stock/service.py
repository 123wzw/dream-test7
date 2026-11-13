"""扣减逻辑。"""

import time

from stock import db

# 模拟真实环境的 IO 延迟（数据库往返），测试里可用 STOCK_DELAY 覆盖
IO_DELAY = 0.005


class InsufficientStock(Exception):
    pass


def _io_delay() -> None:
    time.sleep(IO_DELAY)


def get_stock(sku: str) -> int:
    conn = db.connect()
    try:
        row = conn.execute("SELECT qty FROM stock WHERE sku = ?", (sku,)).fetchone()
        if row is None:
            raise ValueError(f"unknown sku: {sku}")
        return int(row["qty"])
    finally:
        conn.close()


def purchase(order_id: str, sku: str, qty: int) -> int:
    conn = db.connect()
    try:
        row = conn.execute("SELECT qty FROM stock WHERE sku = ?", (sku,)).fetchone()
        if row is None:
            raise ValueError(f"unknown sku: {sku}")
        current = int(row["qty"])

        conn.execute(
            "INSERT INTO orders (order_id, sku, qty) VALUES (?, ?, ?)",
            (order_id, sku, qty),
        )

        _io_delay()

        if current < qty:
            raise InsufficientStock(f"{sku} only {current} left")

        conn.execute("UPDATE stock SET qty = ? WHERE sku = ?", (current - qty, sku))
        return current - qty
    finally:
        conn.close()
