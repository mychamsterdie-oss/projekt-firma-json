from classes.user import User


class Employee(User):
    def __init__(self, username, password, position="Pracownik",
                 salary=0, permissions=None, user_id=None):
        super().__init__(
            username=username,
            password=password,
            role="employee",
            permissions=permissions or ["view_products", "sell"],
            position=position,
            salary=salary,
            user_id=user_id
        )
