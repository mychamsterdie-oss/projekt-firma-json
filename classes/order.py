class Order:
    def __init__(self, product_name, quantity, sold_by, total_price,
                 customer_name="Klient", order_id=None):
        self.id = order_id or f"order-{product_name.lower().replace(' ', '-')}-{quantity}"
        self.product_name = product_name
        self.quantity = quantity
        self.sold_by = sold_by
        self.total_price = float(total_price)
        self.customer_name = customer_name

    def to_dict(self):
        return {
            "id": self.id,
            "product_name": self.product_name,
            "quantity": self.quantity,
            "sold_by": self.sold_by,
            "total_price": self.total_price,
            "customer_name": self.customer_name
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_name=data["product_name"],
            quantity=data["quantity"],
            sold_by=data["sold_by"],
            total_price=data["total_price"],
            customer_name=data.get("customer_name", "Klient"),
            order_id=data.get("id")
        )

    def __str__(self):
        return f"Zamówienie: {self.product_name} x{self.quantity} | Sprzedane przez: {self.sold_by}"
