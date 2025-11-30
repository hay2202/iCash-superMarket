from sqlalchemy import Column, String, Float
from .base import Base

class Product(Base):
    __tablename__ = "products"

    product_name = Column(String, primary_key=True)
    unit_price = Column(Float, nullable=False)

    def __repr__(self):
        return f"<Product {self.product_name} price={self.unit_price}>"
