from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base


class OrderStatus:
    CREATED = 'created'


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    status = Column(String, index=True)
    total = Column(Integer)

    items = relationship("OrderItem", back_populates="order")

