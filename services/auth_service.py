# services/auth_service.py

from database.admin_dao import AdminDAO
from tkinter import messagebox 
class AuthService:
    def __init__(self):
        self.admin_dao = AdminDAO()
        self.current_user = None 

    def login_admin(self, uid: str, username: str, password: str) -> bool:
        if not uid or not username or not password:
            return False

        is_authenticated = self.admin_dao.authenticate_admin(uid, username, password)

        if is_authenticated:
            print(f"Authentication successful for user ID: {uid}")
            return True
        else:
            return False    
    # def logout_admin(self):
    #     self.current_user = None
    #     print("User logged out.")
