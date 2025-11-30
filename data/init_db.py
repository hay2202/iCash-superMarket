import time
import csv
import os

from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError

from cashier.database import engine
from cashier.models.base import Base
from cashier.models.user import User
from cashier.models.product import Product
from cashier.models.purchase import Purchase

DATA_DIR = os.path.dirname(__file__)


def wait_for_db(max_retries=10, delay=2):
    for i in range(max_retries):
        try:
            # try simple connection
            with engine.connect() as conn:
                print("Database is ready!")
                return
        except OperationalError:
            print(f"DB not ready yet... retry ({i+1}/{max_retries})")
            time.sleep(delay)
    raise Exception("Database is not available after retries.")


def init_db():

    print("Waiting for database...")
    wait_for_db()

    print("Creating tables...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    session = Session(bind=engine)

    # Load products
    with open(os.path.join(DATA_DIR, "products_list.csv"), encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            session.add(Product(
                product_name=row["product_name"],
                unit_price=float(row["unit_price"])
            ))

    # Load purchases + unique users
    users = set()
    with open(os.path.join(DATA_DIR, "purchases.csv"), encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for idx, row in enumerate(reader):
            session.add(Purchase(
                id=str(idx),
                supermarket_id=row["supermarket_id"],
                timestamp=row["timestamp"],
                user_id=row["user_id"],
                items_list=row["items_list"],
                total_amount=float(row["total_amount"]),
            ))
            users.add(row["user_id"])

    # Insert users
    for uid in users:
        session.add(User(user_id=uid))

    session.commit()
    session.close()
    print("DB initialization complete!")


if __name__ == "__main__":
    init_db()