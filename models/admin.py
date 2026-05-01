class AdminUser:

    def __init__(
        self,
        user_id: int,
        username: str,
        password_hash: str,
        full_name: str = None,
        is_super_admin: bool = False
    ):

        if not username:
            raise ValueError("Username cannot be empty")

        if not password_hash:
            raise ValueError("Password hash required")

        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash
        self.full_name = full_name
        self.is_super_admin = bool(is_super_admin)

    def __repr__(self):
        return (
            f"AdminUser("
            f"ID={self.user_id}, "
            f"Username='{self.username}', "
            f"SuperAdmin={self.is_super_admin})"
        )

    # 🔒 SAFE OUTPUT (no password)
    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "full_name": self.full_name,
            "is_super_admin": self.is_super_admin
        }

    # ⚠️ Internal use only
    def to_internal_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "full_name": self.full_name,
            "is_super_admin": self.is_super_admin
        }

    @staticmethod
    def from_db_record(record: dict):
        if not record:
            return None

        return AdminUser(
            user_id=record["user_id"],
            username=record["username"],
            password_hash=record["password_hash"],
            full_name=record.get("full_name"),
            is_super_admin=record.get("is_super_admin", 0) == 1
        )