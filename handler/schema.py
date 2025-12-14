# schema.py
import sqlite3


def row_to_dict(row):
    return dict(row) if row else None


class db_tools:

    def __init__(self, db_instance: sqlite3.Connection):
        self.db = db_instance

    # ---------------- PRODUCTS ----------------
    def add_product(self, product_sku: str, prod_name: str, price: float, desc: str):
        try:
            self.db.execute(
                "INSERT INTO products (sku, name, price, description) VALUES (?, ?, ?, ?)",
                (product_sku, prod_name, price, desc)
            )
            self.db.commit()
            return {"status": "success", "message": "Product added"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_product(self, product_id: int):
        try:
            row = self.db.execute(
                "SELECT * FROM products WHERE id = ?",
                (product_id,)
            ).fetchone()
            return {"status": "success", "data": row_to_dict(row)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_all_products(self):
        try:
            rows = self.db.execute("SELECT * FROM products").fetchall()
            return {"status": "success", "data": [dict(r) for r in rows]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- WAREHOUSES ----------------
    def add_warehouse(self, name: str, location: str):
        try:
            self.db.execute(
                "INSERT INTO warehouses (name, location) VALUES (?, ?)",
                (name, location)
            )
            self.db.commit()
            return {"status": "success", "message": "Warehouse added"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_warehouse(self, warehouse_id: int):
        try:
            row = self.db.execute(
                "SELECT * FROM warehouses WHERE id = ?",
                (warehouse_id,)
            ).fetchone()
            return {"status": "success", "data": row_to_dict(row)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_all_warehouses(self):
        try:
            rows = self.db.execute("SELECT * FROM warehouses").fetchall()
            return {"status": "success", "data": [dict(r) for r in rows]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- INVENTORY ----------------
    def add_inventory(self, product_id: int, warehouse_id: int, quantity: int):
        try:
            self.db.execute(
                "INSERT INTO inventory (product_id, warehouse_id, quantity) VALUES (?, ?, ?)",
                (product_id, warehouse_id, quantity)
            )
            self.db.commit()
            return {"status": "success", "message": "Inventory added"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_inventory(self, product_id: int, warehouse_id: int):
        try:
            row = self.db.execute(
                "SELECT * FROM inventory WHERE product_id = ? AND warehouse_id = ?",
                (product_id, warehouse_id)
            ).fetchone()
            return {"status": "success", "data": row_to_dict(row)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_inventory_by_product(self, product_id: int):
        try:
            rows = self.db.execute(
                "SELECT * FROM inventory WHERE product_id = ?",
                (product_id,)
            ).fetchall()
            return {"status": "success", "data": [dict(r) for r in rows]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- ORDERS ----------------
    def add_order(self, order_number: str, status: str):
        try:
            self.db.execute(
                "INSERT INTO orders (order_number, status) VALUES (?, ?)",
                (order_number, status)
            )
            self.db.commit()
            return {"status": "success", "message": "Order added"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_order(self, order_id: int):
        try:
            row = self.db.execute(
                "SELECT * FROM orders WHERE id = ?",
                (order_id,)
            ).fetchone()
            return {"status": "success", "data": row_to_dict(row)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_order_by_number(self, order_number: str):
        try:
            row = self.db.execute(
                "SELECT * FROM orders WHERE order_number = ?",
                (order_number,)
            ).fetchone()
            return {"status": "success", "data": row_to_dict(row)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- ORDER ITEMS ----------------
    def add_order_item(self, order_id: int, product_id: int, quantity: int, price: float):
        try:
            self.db.execute(
                "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                (order_id, product_id, quantity, price)
            )
            self.db.commit()
            return {"status": "success", "message": "Order item added"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_order_items(self, order_id: int):
        try:
            rows = self.db.execute(
                "SELECT * FROM order_items WHERE order_id = ?",
                (order_id,)
            ).fetchall()
            return {"status": "success", "data": [dict(r) for r in rows]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- SHIPMENTS ----------------
    def add_shipment(self, order_id: int, tracking_number: str, status: str):
        try:
            self.db.execute(
                "INSERT INTO shipments (order_id, tracking_number, status) VALUES (?, ?, ?)",
                (order_id, tracking_number, status)
            )
            self.db.commit()
            return {"status": "success", "message": "Shipment added"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_shipment(self, shipment_id: int):
        try:
            row = self.db.execute(
                "SELECT * FROM shipments WHERE id = ?",
                (shipment_id,)
            ).fetchone()
            return {"status": "success", "data": row_to_dict(row)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_shipments_by_order(self, order_id: int):
        try:
            rows = self.db.execute(
                "SELECT * FROM shipments WHERE order_id = ?",
                (order_id,)
            ).fetchall()
            return {"status": "success", "data": [dict(r) for r in rows]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    # ---------------- PAYMENTS ----------------
    def add_payment(self, order_id: int, amount: float, method: str, status: str):
        try:
            self.db.execute(
                "INSERT INTO payments (order_id, amount, method, status) VALUES (?, ?, ?, ?)",
                (order_id, amount, method, status)
            )
            self.db.commit()
            return {"status": "success", "message": "Payment added"}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_payment(self, payment_id: int):
        try:
            row = self.db.execute(
                "SELECT * FROM payments WHERE id = ?",
                (payment_id,)
            ).fetchone()
            return {"status": "success", "data": row_to_dict(row)}
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_payments_by_order(self, order_id: int):
        try:
            rows = self.db.execute(
                "SELECT * FROM payments WHERE order_id = ?",
                (order_id,)
            ).fetchall()
            return {"status": "success", "data": [dict(r) for r in rows]}
        except Exception as e:
            return {"status": "error", "message": str(e)}

