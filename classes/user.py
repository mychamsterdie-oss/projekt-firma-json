class User:
    def __init__(self, username, password, role="employee", permissions=None,
                 position="Pracownik", salary=0, user_id=None):
        self.id = user_id or f"user-{username.lower()}"
        self.username = username
        self.password = password
        self.role = role
        self.permissions = permissions or []
        self.position = position
        self.salary = float(salary)

    def has_permission(self, permission):
        return "all" in self.permissions or permission in self.permissions

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "password": self.password,
            "role": self.role,
            "permissions": self.permissions,
            "position": self.position,
            "salary": self.salary
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            username=data["username"],
            password=data["password"],
            role=data.get("role", "employee"),
            permissions=data.get("permissions", []),
            position=data.get("position", "Pracownik"),
            salary=data.get("salary", 0),
            user_id=data.get("id")
        )

    def __str__(self):
        return f"{self.username} ({self.role})"
