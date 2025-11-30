from sqlalchemy import Column, String, DateTime
from datetime import datetime
from .base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(String, primary_key=True)
    name = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User id={self.user_id}>"