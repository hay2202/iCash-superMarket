import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cashier.models.base import Base
from cashier.models.product import Product
from cashier.models.user import User
from cashier.models.purchase import Purchase
from cashier.services.purchase_service import PurchaseService


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:", echo=False)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()


def test_get_or_create_user_creates_new_user(db_session):
    user, is_new = PurchaseService.get_or_create_user(db_session, "user-1")
    assert is_new is True
    assert user.user_id == "user-1"
    fetched = db_session.query(User).filter(User.user_id == "user-1").one_or_none()
    assert fetched is not None


def test_get_or_create_user_returns_existing_user(db_session):
    u = User(user_id="u2")
    db_session.add(u)
    db_session.commit()

    user, is_new = PurchaseService.get_or_create_user(db_session, "u2")
    assert is_new is False
    assert user.user_id == "u2"


def test_calculate_total_sums_unit_prices(db_session):
    db_session.add_all([
        Product(product_name="apple", unit_price=0.5),
        Product(product_name="banana", unit_price=0.75),
    ])
    db_session.commit()

    total = PurchaseService.calculate_total(db_session, ["apple", "banana", "banana"])
    assert pytest.approx(total, rel=1e-9) == 0.5 + 0.75 + 0.75


def test_calculate_total_raises_on_unknown_product(db_session):
    db_session.add(Product(product_name="milk", unit_price=1.2))
    db_session.commit()

    with pytest.raises(ValueError) as excinfo:
        PurchaseService.calculate_total(db_session, ["milk", "eggs"])

    assert "Unknown product: eggs" in str(excinfo.value)


def test_create_purchase_creates_purchase_and_marks_user_new(db_session):
    db_session.add_all([Product(product_name="bread", unit_price=2.0)])
    db_session.commit()

    purchase, is_new = PurchaseService.create_purchase(db_session, "s1", "user-x", ["bread"])
    assert is_new is True
    assert purchase.supermarket_id == "s1"
    assert purchase.user_id == "user-x"
    assert purchase.total_amount == 2.0
    assert purchase.items_list == "bread"
    assert db_session.query(User).filter(User.user_id == "user-x").one_or_none() is not None
    assert db_session.query(Purchase).filter(Purchase.id == purchase.id).one_or_none() is not None


def test_create_purchase_with_existing_user_returns_false(db_session):
    db_session.add(User(user_id="existing"))
    db_session.add(Product(product_name="gum", unit_price=0.25))
    db_session.commit()

    purchase, is_new = PurchaseService.create_purchase(db_session, "s2", "existing", ["gum", "gum"])
    assert is_new is False
    assert purchase.total_amount == pytest.approx(0.5)


def test_create_purchase_with_empty_items_results_in_zero_total(db_session):
    purchase, is_new = PurchaseService.create_purchase(db_session, "s3", "user-empty", [])
    assert purchase.total_amount == 0
    assert purchase.items_list == ""
    assert is_new is True

