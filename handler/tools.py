import sqlite3
import logging
from fastmcp import FastMCP
from .schema import db_tools

mcp = FastMCP("Order management system")


class MCPTools:
    """
    MCPTools exposes database operations as MCP tools.

    Each tool:
    - Accepts primitive arguments only (int, str, float)
    - Returns JSON-serializable dicts
    - Is safe for agent consumption
    """

    def __init__(self, db_instance: sqlite3.Connection):
        """
        Initialize MCP tools with an active database connection.

        Args:
            db_instance (sqlite3.Connection): Open SQLite connection
        """
        logging.info("Initializing database tools ...")
        self.db = db_tools(db_instance=db_instance)

    def start_mcp(self):
        """
        Starts the MCP server and exposes all tools to agents.
        """
        logging.info("Starting mcp server...")
        mcp.run()

    # -------------------- ADD TOOLS --------------------

    @mcp.tool()
    def add_product(self, product_sku: str, product_name: str, price: float, desc: str):
        """
        Add a new product to the system.

        Args:
            product_sku (str): Unique SKU identifier for the product
            product_name (str): Name of the product
            price (float): Price of the product
            desc (str): Short description of the product

        Returns:
            dict:
                status (str): "success" or "error"
                message (str): Result message
        """
        return self.db.add_product(product_sku, product_name, price, desc)

    @mcp.tool()
    def add_warehouse(self, warehouse_name: str, warehouse_location: str):
        """
        Add a warehouse.

        Args:
            warehouse_name (str): Warehouse name
            warehouse_location (str): Physical location

        Returns:
            dict:
                status (str)
                message (str)
        """
        return self.db.add_warehouse(warehouse_name, warehouse_location)

    @mcp.tool()
    def add_inventory(self, product_id: int, warehouse_id: int, quantity: int):
        """
        Add inventory quantity for a product in a warehouse.

        Args:
            product_id (int): Product ID
            warehouse_id (int): Warehouse ID
            quantity (int): Available quantity

        Returns:
            dict:
                status (str)
                message (str)
        """
        return self.db.add_inventory(product_id, warehouse_id, quantity)

    @mcp.tool()
    def add_order(self, order_number: str, status: str):
        """
        Create a new order.

        Args:
            order_number (str): Unique order identifier
            status (str): Order status (e.g., CREATED, PAID, SHIPPED)

        Returns:
            dict:
                status (str)
                message (str)
        """
        return self.db.add_order(order_number, status)

    @mcp.tool()
    def add_order_item(self, order_id: int, product_id: int, quantity: int, price: float):
        """
        Add an item to an order.

        Args:
            order_id (int): Order ID
            product_id (int): Product ID
            quantity (int): Quantity ordered
            price (float): Price per unit

        Returns:
            dict:
                status (str)
                message (str)
        """
        return self.db.add_order_item(order_id, product_id, quantity, price)

    @mcp.tool()
    def add_shipment(self, order_id: int, tracking_number: str, status: str):
        """
        Add shipment details for an order.

        Args:
            order_id (int): Order ID
            tracking_number (str): Courier tracking number
            status (str): Shipment status

        Returns:
            dict:
                status (str)
                message (str)
        """
        return self.db.add_shipment(order_id, tracking_number, status)

    @mcp.tool()
    def add_payment(self, order_id: int, amount: float, method: str, status: str):
        """
        Record a payment for an order.

        Args:
            order_id (int): Order ID
            amount (float): Paid amount
            method (str): Payment method (UPI, CARD, COD, etc.)
            status (str): Payment status (SUCCESS, FAILED)

        Returns:
            dict:
                status (str)
                message (str)
        """
        return self.db.add_payment(order_id, amount, method, status)

    # -------------------- GET TOOLS --------------------

    @mcp.tool()
    def get_product(self, product_id: int):
        """
        Fetch product details by product ID.

        Args:
            product_id (int): Product ID

        Returns:
            dict:
                status (str)
                data (dict | null): Product details
        """
        return self.db.get_product(product_id)

    @mcp.tool()
    def get_all_products(self):
        """
        Fetch all products.

        Returns:
            dict:
                status (str)
                data (list[dict]): List of products
        """
        return self.db.get_all_products()

    @mcp.tool()
    def get_warehouse(self, warehouse_id: int):
        """
        Fetch warehouse details.

        Args:
            warehouse_id (int): Warehouse ID

        Returns:
            dict:
                status (str)
                data (dict | null)
        """
        return self.db.get_warehouse(warehouse_id)

    @mcp.tool()
    def get_all_warehouses(self):
        """
        Fetch all warehouses.

        Returns:
            dict:
                status (str)
                data (list[dict])
        """
        return self.db.get_all_warehouses()

    @mcp.tool()
    def get_inventory(self, product_id: int, warehouse_id: int):
        """
        Fetch inventory for a product in a warehouse.

        Args:
            product_id (int)
            warehouse_id (int)

        Returns:
            dict:
                status (str)
                data (dict | null)
        """
        return self.db.get_inventory(product_id, warehouse_id)

    @mcp.tool()
    def get_inventory_by_product(self, product_id: int):
        """
        Fetch inventory across warehouses for a product.

        Args:
            product_id (int)

        Returns:
            dict:
                status (str)
                data (list[dict])
        """
        return self.db.get_inventory_by_product(product_id)

    @mcp.tool()
    def get_order(self, order_id: int):
        """
        Fetch order by ID.

        Args:
            order_id (int)

        Returns:
            dict:
                status (str)
                data (dict | null)
        """
        return self.db.get_order(order_id)

    @mcp.tool()
    def get_order_by_number(self, order_number: str):
        """
        Fetch order using order number.

        Args:
            order_number (str)

        Returns:
            dict:
                status (str)
                data (dict | null)
        """
        return self.db.get_order_by_number(order_number)

    @mcp.tool()
    def get_order_items(self, order_id: int):
        """
        Fetch all items belonging to an order.

        Args:
            order_id (int)

        Returns:
            dict:
                status (str)
                data (list[dict])
        """
        return self.db.get_order_items(order_id)

    @mcp.tool()
    def get_shipment(self, shipment_id: int):
        """
        Fetch shipment details.

        Args:
            shipment_id (int)

        Returns:
            dict:
                status (str)
                data (dict | null)
        """
        return self.db.get_shipment(shipment_id)

    @mcp.tool()
    def get_shipments_by_order(self, order_id: int):
        """
        Fetch all shipments for an order.

        Args:
            order_id (int)

        Returns:
            dict:
                status (str)
                data (list[dict])
        """
        return self.db.get_shipments_by_order(order_id)

    @mcp.tool()
    def get_payment(self, payment_id: int):
        """
        Fetch payment details.

        Args:
            payment_id (int)

        Returns:
            dict:
                status (str)
                data (dict | null)
        """
        return self.db.get_payment(payment_id)

    @mcp.tool()
    def get_payments_by_order(self, order_id: int):
        """
        Fetch all payments for an order.

        Args:
            order_id (int)

        Returns:
            dict:
                status (str)
                data (list[dict])
        """
        return self.db.get_payments_by_order(order_id)

