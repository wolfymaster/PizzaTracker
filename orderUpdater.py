import click
import requests
from db.db import SessionLocal, engine, Base
from pizzaTracker import schema
from db.models.order import Order, OrderStatus
from db.models.orderItem import OrderItem

PORT = 8000

@click.group()
def cli():
    pass


@cli.command()
def view_orders():
    session = SessionLocal()

    orders = session.query(Order).all()

    order_ids = [order.id for order in orders]
    selected_order_id = click.prompt(
        "Select an order", type=click.Choice(list(map(str, order_ids)))
    )

    selected_order = session.query(Order).filter_by(id=selected_order_id).one()

    statuses = ["Preparing", "Baking", "Ready"]
    selected_status = click.prompt(
        "Select a status", type=click.Choice(statuses)
    )

    payload = {"id": selected_order_id, "status": selected_status}
    response = requests.post(f"http://localhost:{PORT}/update", json=payload)

    click.echo(f"Status updated to {selected_status}")

if __name__ == '__main__':
    view_orders()