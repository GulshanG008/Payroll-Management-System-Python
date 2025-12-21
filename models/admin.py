# models/admin.py

class AdminUser:
    def __init__(
        self,
        user_id: int,
        username: str,
        password_hash: str,
        full_name: str = None,
        is_super_admin: bool = False
    ):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.full_name = full_name
        self.is_super_admin = is_super_admin

    def __repr__(self):
        return (
            f"AdminUser("
            f"ID={self.user_id}, "
            f"Username='{self.username}', "
            f"SuperAdmin={self.is_super_admin})"
        )

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "full_name": self.full_name,
            "is_super_admin": self.is_super_admin
        }

    @staticmethod
    def from_db_record(record: dict):
        return AdminUser(
            user_id=record.get("user_id"),
            username=record.get("username"),
            password_hash=record.get("password_hash"),
            full_name=record.get("full_name"),
            is_super_admin=bool(record.get("is_super_admin"))
        )
