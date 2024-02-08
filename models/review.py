from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.schema import ForeignKey
from core.database import Base
from datetime import datetime


class ReviewModel(Base):
    __tablename__ = "review"

    id = Column(Integer, primary_key=True)
    name = Column(String(200))
    comment = Column(String(255))
    rating = Column(Integer)

    user_id = Column(Integer, ForeignKey('user.id'))


    product_id = Column(Integer, ForeignKey("product.id"))

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
