# services/auth_service.py

from database.admin_dao import AdminDAO
from tkinter import messagebox # Used for showing user-friendly errors

class AuthService:
    """
    Handles the business logic for user authentication and authorization.
    It interacts with the AdminDAO to verify credentials.
    """
    def __init__(self):
        # Instantiate the DAO to gain access to database methods
        self.admin_dao = AdminDAO()
        # You can also initialize a variable here to hold the currently logged-in user object, if needed.
        self.current_user = None 

    def login_admin(self, uid: str, username: str, password: str) -> bool:
        """
        Attempts to authenticate an administrator.

        Args:
            uid (str): The user's ID.
            username (str): The user's provided username.
            password (str): The user's provided password (should be plain text here, 
                            as hashing verification happens internally or in the DAO).

        Returns:
            bool: True if authentication is successful, False otherwise.
        """
        # 1. Input Validation (Basic sanity check)
        if not uid or not username or not password:
            # While the GUI might catch this, the service should also validate input
            return False

        # 2. Call the DAO for credential verification
        # The DAO handles the connection and the raw comparison (SQL logic)
        is_authenticated = self.admin_dao.authenticate_admin(uid, username, password)

        if is_authenticated:
            # 3. Success Logic (Business Rules)
            # In a real application, you would fetch the full AdminUser object here 
            # and store it in self.current_user for later authorization checks.
            print(f"Authentication successful for user ID: {uid}")
            # Example: self.current_user = self.admin_dao.get_admin_user_by_id(uid)
            return True
        else:
            # 4. Failure Logic
            # The AdminDAO will print a database error if one occurs, 
            # but the service determines the final result.
            return False
            
    # You might include other methods here, such as:
    
    # def logout_admin(self):
    #     self.current_user = None
    #     print("User logged out.")
        
    # def authorize_action(self, required_role: str) -> bool:
    #     """Checks if the current user has permission for a specific action."""
    #     # if self.current_user and self.current_user.is_super_admin: return True
    #     # ...
    #     pass