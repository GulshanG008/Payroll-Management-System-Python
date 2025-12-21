# services/auth_service.py

import hashlib
from database.admin_dao import AdminDAO


class AuthService:
    """
    Handles authentication logic for admin users.
    """

    def __init__(self):
        self.admin_dao = AdminDAO()
        self.current_user = None

    def login_admin(self, username: str, password: str) -> bool:
        """
        Authenticate admin using username and password.
        """

        if not username or not password:
            return False

        admin = self.admin_dao.get_by_username(username)
        if not admin:
            return False

        password_hash = hashlib.sha256(password.encode()).hexdigest()

        if admin["password_hash"] == password_hash:
            self.current_user = {
                "admin_id": admin["admin_id"],
                "username": admin["username"]
            }
            return True

        return False

    def logout_admin(self):
        """
        Logout current admin.
        """
        self.current_user = None
