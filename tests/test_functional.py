"""库存服务功能测试（单线程）。"""

import os
import tempfile

_TMP = tempfile.mkdtemp(prefix="stock-test-")
os.environ["STOCK_DB"] = os.path.join(_TMP, "stock.db")

import pytest  # noqa: E402

from stock import db, service  # noqa: E402


@pytest.fixture(autouse=True)
def fresh():
    db.init_db()
    db.reset({"SKU-A": 10, "SKU-B": 0})
    service.IO_DELAY = 0
    yield


def test_purchase_decreases_stock():
    remaining = service.purchase("o-1", "SKU-A", 3)
    assert remaining == 7
    assert service.get_stock("SKU-A") == 7


def test_purchase_more_than_stock_raises():
    with pytest.raises(service.InsufficientStock):
        service.purchase("o-2", "SKU-A", 99)


def test_purchase_zero_stock_raises():
    with pytest.raises(service.InsufficientStock):
        service.purchase("o-3", "SKU-B", 1)


def test_unknown_sku_raises():
    with pytest.raises(ValueError):
        service.purchase("o-4", "SKU-Z", 1)


def test_get_stock_reads_value():
    assert service.get_stock("SKU-A") == 10
