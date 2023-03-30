# # Import the necessary packages
# from consolemenu import *
# from consolemenu.items import *

# # Create the menu
# menu = ConsoleMenu("Title", "Subtitle")

# # Create some items

# # MenuItem is the base class for all items, it doesn't do anything when selected
# menu_item = MenuItem("Menu Item")

# # A FunctionItem runs a Python function when selected
# function_item = FunctionItem("Call a Python function", input, ["Enter an input"])

# # A CommandItem runs a console command
# command_item = CommandItem("Run a console command",  "touch hello.txt")

# # A SelectionMenu constructs a menu from a list of strings
# selection_menu = SelectionMenu(["item1", "item2", "item3"])

# # A SubmenuItem lets you add a menu (the selection_menu above, for example)
# # as a submenu of another menu
# submenu_item = SubmenuItem("Submenu item", selection_menu, menu)

# # Once we're done creating them, we just add the items to the menu
# menu.append_item(menu_item)
# menu.append_item(function_item)
# menu.append_item(command_item)
# menu.append_item(submenu_item)

# # Finally, we call show to show the menu and allow the user to interact
# menu.show()

import click
import requests
from db.db import SessionLocal, engine, Base
from .pizzaTracker import schema
from db.models.order import Order, OrderStatus
from db.models.orderItem import OrderItem


@click.group()
def cli():
    pass


@cli.command()
def view_orders():
    engine = create_engine("sqlite:///orders.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    orders = session.query(Order).all()

    order_ids = [order.id for order in orders]
    selected_order_id = click.prompt(
        "Select an order", type=click.Choice(map(str, order_ids))
    )

    selected_order = session.query(Order).filter_by(id=selected_order_id).one()

    statuses = ["Preparing", "Baking", "Ready"]
    selected_status = click.prompt(
        "Select a status", type=click.Choice(statuses)
    )

    payload = {"id": selected_order_id, "status": selected_status}
    response = requests.post("http://localhost/update", json=payload)

    click.echo(f"Status updated to {selected_status}")