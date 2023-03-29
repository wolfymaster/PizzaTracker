from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from ..db import Base


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    price = Column(Integer)
    quantity = Column(Integer)
    order_id = Column(Integer, ForeignKey("orders.id"))

    order = relationship("Order", back_populates="items")
