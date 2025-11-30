from sqlalchemy import Column, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .base import Base

class Purchase(Base):
    __tablename__ = "purchases"

    id = Column(String, primary_key=True)
    supermarket_id = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)
    user_id = Column(String, ForeignKey("users.user_id"))
    items_list = Column(String)
    total_amount = Column(Float)

    user = relationship("User")

    def __repr__(self):
        return f"<Purchase id={self.id} user={self.user_id} total={self.total_amount}>"