"""演示数据。"""

from stock import db


def main() -> None:
    db.init_db()
    db.reset({"SKU-A": 10, "SKU-B": 0})
    print("seeded: SKU-A=10, SKU-B=0")


if __name__ == "__main__":
    main()
