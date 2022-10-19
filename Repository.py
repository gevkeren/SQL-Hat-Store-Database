import sqlite3
import sys

from DAO import Hats
from DAO import Suppliers
from DAO import Orders


class Repository:
    def __init__(self, database):
        self.conn = sqlite3.connect(database)
        self.hats = Hats(self.conn)
        self.suppliers = Suppliers(self.conn)
        self.orders = Orders(self.conn)

    def __del__(self):
        self.conn.commit()
        self.conn.close()

    def create_tables(self):

        self.conn.executescript("""
        CREATE TABLE IF NOT EXISTS suppliers(
            id          INT     PRIMARY KEY,
            name        TEXT    NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS hats(
            id          INT     PRIMARY KEY,
            topping     TEXT    NOT NULL,
            supplier    INT     REFERENCES suppliers(suppliers_id),
            quantity    INT     NOT NULL
        );
        
        CREATE TABLE IF NOT EXISTS orders(
            id          INT     PRIMARY KEY,
            location    TEXT    NOT NULL,
            hat         INT     REFERENCES hats(hat_id)
        );
    """)

    def deliver(self, location, topping, order_id):
        # adding the order to the orders table
        hat_id = self.hats.get_lowest_id_by_topping(topping)
        self.orders.insert(order_id, location, hat_id)

        # updating the hats table
        decreased_quantity = self.hats.get_quantity_by_id(hat_id)
        if decreased_quantity == 0:
            self.hats.delete(hat_id)
        else:
            self.hats.update_quantity(hat_id)

