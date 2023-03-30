import json

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
from db.db import SessionLocal, engine, Base
from . import schema
from db.models.order import Order, OrderStatus
from db.models.orderItem import OrderItem

Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:9000",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

@app.post("/update", response_model=schema.Order)
async def update(request: schema.UpdateOrderStatusRequest, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.id == request.id).first()

    if order:
        order.status = request.status
        db.commit()
        db.refresh(order)
        return order
    else:
        return {"message": f"Order with id {request.id} not found"}

@app.get("/orders", response_model=List[schema.Order])
def get_orders(skip: int = 0, limit: int = 100, db = Depends(get_db)):
    # Retrieve the orders from the database
    orders = db.query(Order).offset(skip).limit(limit).all()
    return orders