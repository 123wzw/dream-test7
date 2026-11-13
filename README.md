# stock-service

库存扣减服务，供订单系统调用。

## 技术栈

- Python 3.12，纯标准库（sqlite3 / threading）

## 初始化

```bash
python -m venv .venv
.venv/Scripts/python -m pip install -r requirements.txt

# 建库并写入演示数据：SKU-A 库存 10、SKU-B 库存 0
.venv/Scripts/python -m stock.seed
```

## 用法

```python
from stock.service import purchase

purchase(order_id="o-1001", sku="SKU-A", qty=2)
```

扣减成功返回剩余库存；库存不足抛 `InsufficientStock`。

## 目录

```
stock/db.py       连接与建表
stock/service.py  扣减逻辑
stock/seed.py     演示数据
docs/RULES.md     并发与一致性要求
tests/test_functional.py  功能测试
```

## 测试

```bash
.venv/Scripts/python -m pytest -q
```

## 已知问题

- 大促期间出现过超卖，客服收到过「库存扣成负数」的投诉。
- 支付回调重试时，同一笔订单被扣了两次。
