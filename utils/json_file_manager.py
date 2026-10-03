from pathlib import Path

from classes.admin import Admin
from classes.employee import Employee
from classes.order import Order
from classes.product import Product
from utils.json_file_manager import load_json, save_json


class Company:
    def __init__(self, company_name="Firma XYZ"):
        self.company_name = company_name
        self.base_dir = Path(__file__).resolve().parent.parent
        self.data_dir = self.base_dir / "data"

        self.users_path = self.data_dir / "users.json"
        self.products_path = self.data_dir / "products.json"
        self.finances_path = self.data_dir / "finances.json"
        self.orders_path = self.data_dir / "orders.json"

        self._ensure_data_files()
        self.users = self._load_users()
        self.products = self._load_products()
        self.finances = self._load_finances()
        self.orders = self._load_orders()

    def _ensure_data_files(self):
        self.data_dir.mkdir(parents=True, exist_ok=True)

        default_users = [
            {
                "id": "admin-1",
                "username": "admin",
                "password": "admin123",
                "role": "admin",
                "permissions": ["all"],
                "position": "Administrator",
                "salary": 0
            },
            {
                "id": "emp-1",
                "username": "manager",
                "password": "manager123",
                "role": "employee",
                "permissions": ["view_products", "manage_products", "view_finances"],
                "position": "Manager",
                "salary": 5000
            },
            {
                "id": "emp-2",
                "username": "seller",
                "password": "seller123",
                "role": "employee",
                "permissions": ["view_products", "sell"],
                "position": "Sprzedawca",
                "salary": 3500
            }
        ]

        default_products = [
            {"id": "prod-1", "name": "Laptop", "price": 3200.0, "stock": 8, "category": "Elektronika"},
            {"id": "prod-2", "name": "Smartfon", "price": 1800.0, "stock": 15, "category": "Elektronika"},
            {"id": "prod-3", "name": "Klawiatura", "price": 250.0, "stock": 30, "category": "Akcesoria"}
        ]

        default_finances = {
            "company_name": self.company_name,
            "cash": 50000.0,
            "profit": 0.0,
            "expenses": 0.0
        }

        if not self.users_path.exists():
            save_json(self.users_path, default_users)
        if not self.products_path.exists():
            save_json(self.products_path, default_products)
        if not self.finances_path.exists():
            save_json(self.finances_path, default_finances)
        if not self.orders_path.exists():
            save_json(self.orders_path, [])

    def _load_users(self):
        data = load_json(self.users_path)
        users = []
        for item in data:
            if item.get("role") == "admin":
                users.append(Admin(username=item["username"], password=item["password"], user_id=item.get("id")))
            else:
                users.append(Employee(
                    username=item["username"],
                    password=item["password"],
                    position=item.get("position", "Pracownik"),
                    salary=item.get("salary", 0),
                    permissions=item.get("permissions", ["view_products", "sell"]),
                    user_id=item.get("id")
                ))
        return users

    def _load_products(self):
        data = load_json(self.products_path)
        return [Product.from_dict(item) for item in data]

    def _load_finances(self):
        data = load_json(self.finances_path)
        if not data:
            return {"company_name": self.company_name, "cash": 0.0, "profit": 0.0, "expenses": 0.0}
        return data

    def _load_orders(self):
        data = load_json(self.orders_path)
        return [Order.from_dict(item) for item in data]

    def save_users(self):
        save_json(self.users_path, [user.to_dict() for user in self.users])

    def save_products(self):
        save_json(self.products_path, [product.to_dict() for product in self.products])

    def save_finances(self):
        save_json(self.finances_path, self.finances)

    def save_orders(self):
        save_json(self.orders_path, [order.to_dict() for order in self.orders])

    def login(self, username, password):
        for user in self.users:
            if user.username == username and user.password == password:
                return user
        return None

    def get_user_by_username(self, username):
        for user in self.users:
            if user.username == username:
                return user
        return None

    def add_user(self, user):
        if self.get_user_by_username(user.username):
            return False
        self.users.append(user)
        self.save_users()
        return True

    def update_user(self, username, **changes):
        user = self.get_user_by_username(username)
        if not user:
            return False

        for key, value in changes.items():
            if key == "permissions" and isinstance(value, str):
                value = [p.strip() for p in value.split(",") if p.strip()]
            if key == "role" and value == "admin":
                user.permissions = ["all"]
            elif key == "role" and value == "employee":
                if not user.permissions:
                    user.permissions = ["view_products", "sell"]
            setattr(user, key, value)

        if user.role == "admin":
            user.permissions = ["all"]

        self.save_users()
        return True

    def get_product_by_name(self, name):
        for product in self.products:
            if product.name.lower() == name.lower():
                return product
        return None

    def add_product(self, product):
        existing = self.get_product_by_name(product.name)
        if existing:
            existing.stock += product.stock
            existing.price = product.price
            self.save_products()
            return True

        self.products.append(product)
        self.save_products()
        return True

    def sell_product(self, product_name, quantity, employee_username, customer_name="Klient"):
        product = self.get_product_by_name(product_name)
        employee = self.get_user_by_username(employee_username)

        if not product:
            return {"success": False, "message": "Produkt nie istnieje."}
        if not employee:
            return {"success": False, "message": "Pracownik nie istnieje."}
        if not employee.has_permission("sell") and not employee.has_permission("all"):
            return {"success": False, "message": "Pracownik nie ma uprawnień do sprzedaży."}
        if quantity <= 0:
            return {"success": False, "message": "Ilość musi być większa od zera."}
        if quantity > product.stock:
            return {"success": False, "message": f"Za mało produktu na magazynie. Dostępnych: {product.stock}"}

        total_price = product.price * quantity
        product.stock -= quantity

        order = Order(
            product_name=product.name,
            quantity=quantity,
            sold_by=employee.username,
            total_price=total_price,
            customer_name=customer_name
        )

        self.orders.append(order)
        self.finances["cash"] = float(self.finances.get("cash", 0.0)) + total_price
        self.finances["profit"] = float(self.finances.get("profit", 0.0)) + total_price

        self.save_products()
        self.save_orders()
        self.save_finances()

        return {
            "success": True,
            "message": f"Sprzedano {quantity} szt. {product.name} za {total_price:.2f} zł.",
            "order": order
        }

    def generate_report(self):
        lines = []
        lines.append("=" * 60)
        lines.append(f"RAPORT FIRMY: {self.company_name}")
        lines.append("=" * 60)
        lines.append("FINANSE:")
        lines.append(f"- Gotówka: {self.finances.get('cash', 0.0):.2f} zł")
        lines.append(f"- Zysk: {self.finances.get('profit', 0.0):.2f} zł")
        lines.append(f"- Koszty: {self.finances.get('expenses', 0.0):.2f} zł")
        lines.append("")
        lines.append("UŻYTKOWNICY:")
        for user in self.users:
            permissions = ", ".join(user.permissions) if user.permissions else "brak"
            lines.append(f"- {user.username} | Rola: {user.role} | Stanowisko: {user.position} | Uprawnienia: {permissions}")

        lines.append("")
        lines.append("PRODUKTY:")
        for product in self.products:
            lines.append(f"- {product.name} | Cena: {product.price:.2f} zł | Ilość: {product.stock} | Kategoria: {product.category}")

        lines.append("")
        lines.append("SPRZEDAŻE:")
        if not self.orders:
            lines.append("- Brak sprzedaży.")
        else:
            for order in self.orders:
                lines.append(f"- {order.product_name} x{order.quantity} | Sprzedane przez: {order.sold_by} | Łącznie: {order.total_price:.2f} zł")

        lines.append("=" * 60)
        return "\n".join(lines)
