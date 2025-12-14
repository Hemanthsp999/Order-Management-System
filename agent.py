import re
from handler.tools import MCPTools

prompt = """
You are an Order Management AI.

You have access to tools that can:
- add products
- manage warehouses
- manage inventory
- create orders
- add order items
- handle payments
- handle shipments

Rules:
- If the user asks to create or update data, you MUST call the correct tool.
- Do NOT invent data.
- Ask for missing required fields.
- Always return tool results.
"""


class OMSAgent:
    """
    OMSAgent understands user intent and calls MCP tools accordingly.
    """

    def __init__(self, tools):
        self.tools = tools

    def handle(self, user_input: str):
        """
        Main agent entrypoint.
        Takes natural language input and routes to MCP tools.
        """
        text = user_input.lower()

        # ---------- PRODUCT ----------
        if "add product" in text:
            return self._add_product(text)

        if "get product" in text:
            return self._get_product(text)

        # ---------- WAREHOUSE ----------
        if "add warehouse" in text:
            return self._add_warehouse(text)

        # ---------- ORDER ----------
        if "create order" in text:
            return self._add_order(text)

        if "add item" in text:
            return self._add_order_item(text)

        # ---------- PAYMENT ----------
        if "make payment" in text:
            return self._add_payment(text)

        # ---------- SHIPMENT ----------
        if "ship order" in text:
            return self._add_shipment(text)

        return {"status": "error", "message": "Unknown command"}

    # ================= PARSERS =================

    def _add_product(self, text: str):
        """
        Example input:
        'add product sku=SKU1 name=mouse price=500 desc=wireless'
        """
        sku = self._extract("sku", text)
        name = self._extract("name", text)
        price = float(self._extract("price", text))
        desc = self._extract("desc", text)

        return self.tools.add_product(sku, name, price, desc)

    def _get_product(self, text: str):
        """
        Example:
        'get product id=1'
        """
        product_id = int(self._extract("id", text))
        return self.tools.get_product(product_id)

    def _add_warehouse(self, text: str):
        """
        'add warehouse name=wh1 location=bangalore'
        """
        name = self._extract("name", text)
        location = self._extract("location", text)
        return self.tools.add_warehouse(name, location)

    def _add_order(self, text: str):
        """
        'create order number=ORD1 status=CREATED'
        """
        number = self._extract("number", text)
        status = self._extract("status", text)
        return self.tools.add_order(number, status)

    def _add_order_item(self, text: str):
        """
        'add item order_id=1 product_id=1 qty=2 price=500'
        """
        return self.tools.add_order_item(
            order_id=int(self._extract("order_id", text)),
            product_id=int(self._extract("product_id", text)),
            quantity=int(self._extract("qty", text)),
            price=float(self._extract("price", text)),
        )

    def _add_payment(self, text: str):
        """
        'make payment order_id=1 amount=1000 method=upi status=SUCCESS'
        """
        return self.tools.add_payment(
            order_id=int(self._extract("order_id", text)),
            amount=float(self._extract("amount", text)),
            method=self._extract("method", text),
            status=self._extract("status", text),
        )

    def _add_shipment(self, text: str):
        """
        'ship order order_id=1 tracking=TRACK1 status=SHIPPED'
        """
        return self.tools.add_shipment(
            order_id=int(self._extract("order_id", text)),
            tracking_number=self._extract("tracking", text),
            status=self._extract("status", text),
        )

    # ================= UTIL =================

    def _extract(self, key: str, text: str):
        match = re.search(rf"{key}=([^\s]+)", text)
        if not match:
            raise ValueError(f"Missing {key}")
        return match.group(1)

