import os
import pytest
from database.db import init_db, close_db
from handler.schema import db_tools

TEST_DB = "database/oms.db"


@pytest.fixture(scope="function")
def db():
    # fresh DB for every test
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)

    conn = init_db(TEST_DB)
    tools = db_tools(conn)

    yield tools

    close_db(conn)
    if os.path.exists(TEST_DB):
        os.remove(TEST_DB)


# ---------------- PRODUCTS ----------------

def test_add_and_get_product(db):
    res = db.add_product("SKU001", "Laptop", 50000, "Gaming laptop")
    assert res["status"] == "success"

    prod = db.get_product(1)
    assert prod["data"]["name"] == "Laptop"


def test_duplicate_product_sku(db):
    db.add_product("SKU001", "Laptop", 50000, "Gaming laptop")
    res = db.add_product("SKU001", "Laptop2", 60000, "Another laptop")
    assert res["status"] == "error"


# ---------------- WAREHOUSES ----------------

def test_add_warehouse(db):
    res = db.add_warehouse("WH1", "Bangalore")
    assert res["status"] == "success"

    wh = db.get_warehouse(1)
    assert wh["data"]["location"] == "Bangalore"


# ---------------- INVENTORY ----------------

def test_inventory_flow(db):
    db.add_product("SKU002", "Mouse", 500, "Wireless mouse")
    db.add_warehouse("WH1", "Bangalore")

    res = db.add_inventory(1, 1, 100)
    assert res["status"] == "success"

    inv = db.get_inventory(1, 1)
    assert inv["data"]["quantity"] == 100


def test_duplicate_inventory_entry(db):
    db.add_product("SKU003", "Keyboard", 1500, "Mechanical")
    db.add_warehouse("WH1", "Bangalore")

    db.add_inventory(1, 1, 50)
    res = db.add_inventory(1, 1, 50)
    assert res["status"] == "error"


# ---------------- ORDERS ----------------

def test_order_creation(db):
    res = db.add_order("ORD001", "CREATED")
    assert res["status"] == "success"

    order = db.get_order_by_number("ORD001")
    assert order["data"]["status"] == "CREATED"


def test_duplicate_order_number(db):
    db.add_order("ORD001", "CREATED")
    res = db.add_order("ORD001", "CREATED")
    assert res["status"] == "error"


# ---------------- ORDER ITEMS ----------------

def test_order_items(db):
    db.add_product("SKU004", "Phone", 30000, "Smartphone")
    db.add_order("ORD002", "CREATED")

    res = db.add_order_item(1, 1, 2, 30000)
    assert res["status"] == "success"

    items = db.get_order_items(1)
    assert len(items["data"]) == 1


# ---------------- PAYMENTS ----------------

def test_payment_flow(db):
    db.add_order("ORD003", "CREATED")

    res = db.add_payment(1, 30000, "UPI", "SUCCESS")
    assert res["status"] == "success"

    payments = db.get_payments_by_order(1)
    assert payments["data"][0]["status"] == "SUCCESS"


# ---------------- SHIPMENTS ----------------

def test_shipment_flow(db):
    db.add_order("ORD004", "PAID")

    res = db.add_shipment(1, "TRACK123", "SHIPPED")
    assert res["status"] == "success"

    ship = db.get_shipments_by_order(1)
    assert ship["data"][0]["tracking_number"] == "TRACK123"

