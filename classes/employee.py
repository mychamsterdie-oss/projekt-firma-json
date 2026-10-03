from classes.user import User


class Employee(User):
    def __init__(self, username, password, position="Pracownik",
                 salary=0, permissions=None, user_id=None):
        default_permissions = ["view_products", "sell"]
        super().__init__(
            username=username,
            password=password,
            role="employee",
            permissions=permissions or default_permissions,
            position=position,
            salary=salary,
            user_id=user_id
        )
