from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from cashier.database import SessionLocal
from cashier.models.product import Product

router = APIRouter(
    prefix="/product",
    tags=["product"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/all")
def get_all_products(db: Session = Depends(get_db)):
    """Get all products from database"""
    try:
        products = db.query(Product).all()
        return {
            "products": [
                {
                    "name": p.product_name,
                    "price": float(p.unit_price)
                }
                for p in products
            ]
        }
    except Exception as e:
        raise Exception(f"Error fetching products: {str(e)}")

