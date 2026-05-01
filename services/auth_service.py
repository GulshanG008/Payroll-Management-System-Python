import hashlib
from config.settings import SECURITY
from database.admin_dao import AdminDAO


class AuthService:

    def __init__(self):
        self.admin_dao = AdminDAO()
        self.current_user = None

    def _hash_password(self, password: str) -> str:
        algo = SECURITY["hash_algorithm"]

        if algo == "sha256":
            return hashlib.sha256(password.encode()).hexdigest()

        raise ValueError("Unsupported hash algorithm")

    def login_admin(self, username: str, password: str) -> bool:

        if not username or not password:
            raise ValueError("Username and password required")

        try:
            admin = self.admin_dao.get_by_username(username)
        except Exception as e:
            raise Exception(f"Database error: {e}")

        if not admin:
            return False

        password_hash = self._hash_password(password)

        if admin["password_hash"] == password_hash:
            self.current_user = {
                "admin_id": admin["admin_id"],
                "username": admin["username"],
            }
            return True

        return False

    def logout_admin(self):
        self.current_user = None

    def is_logged_in(self) -> bool:
        return self.current_user is not None