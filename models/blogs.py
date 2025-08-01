from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from core.database import Base

from enum import Enum as E

class ClassType(E):
    Accepted = "Accepted"
    Pending = "Pending"
    Canceled = "Canceled"


class Blogs(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(String(1000))
    body = Column(String(1000))
    # owner_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    # category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)

    status = Column(Enum(ClassType), default=ClassType.Pending)


    # owner = relationship("User", back_populates="products")
    # category = relationship("Category", back_populates="products")
