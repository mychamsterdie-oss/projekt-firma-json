class Product:
    def __init__(self, name, price, stock, category="Ogólne", product_id=None):
        self.id = product_id or f"prod-{name.lower().replace(' ', '-')}"
        self.name = name
        self.price = float(price)
        self.stock = int(stock)
        self.category = category

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "price": self.price,
            "stock": self.stock,
            "category": self.category
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            price=data["price"],
            stock=data["stock"],
            category=data.get("category", "Ogólne"),
            product_id=data.get("id")
        )

    def __str__(self):
        return f"{self.name} - {self.price} zł | Stan: {self.stock}"
