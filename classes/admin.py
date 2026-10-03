from classes.user import User


class Admin(User):
    def __init__(self, username, password, user_id=None):
        super().__init__(
            username=username,
            password=password,
            role="admin",
            permissions=["all"],
            position="Administrator",
            salary=0,
            user_id=user_id
        )
