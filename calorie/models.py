from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import DateTime
from database import Base

class Item(Base):
    __tablename__ = "items"

    item_name = Column(String, primary_key=True)
    calories = Column(Integer)
    created_at =Column(DateTime, default=datetime.utcnow, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="items")
    
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    items = relationship("Item", back_populates="owner")

