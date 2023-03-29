import json

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session
from db.db import SessionLocal, engine, Base
from . import schema
from db.models.order import Order, OrderStatus
from db.models.orderItem import OrderItem

Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    return db


@app.post("/create", response_model=schema.Order)
async def create(payload: schema.OrderCreate, db: Session = Depends(get_db)):
    order = Order(status=OrderStatus.CREATED, total=payload.total)
    db.add(order)
    db.flush()

    for item in payload.items:
        order_item = OrderItem(**item.dict(), order_id=order.id)
        db.add(order_item)

    db.commit()
    db.refresh(order)

    return order
