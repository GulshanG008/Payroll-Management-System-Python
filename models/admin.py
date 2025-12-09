# models/admin.py

class AdminUser:
    """
    Data model for an Admin User record.
    Represents a row from the 'admin_users' database table.
    Note: Passwords should always be handled as hashes (or salted hashes) 
    in a real application, though the DAO currently uses plain text for simplicity.
    """
    def __init__(self, user_id: int, username: str, password_hash: str, 
                 full_name: str = None, is_super_admin: bool = False):
        self.user_id = user_id
        self.username = username
        self.password_hash = password_hash  # The stored, hashed credential
        self.full_name = full_name
        self.is_super_admin = is_super_admin

    def __repr__(self):
        """Provides a helpful string representation for debugging."""
        return f"AdminUser(ID={self.user_id}, Username='{self.username}', SuperAdmin={self.is_super_admin})"

    def to_dict(self):
        """
        Converts the AdminUser object into a dictionary.
        Note: The password_hash is included here, but should be stripped 
        before sending to any front-end/GUI component.
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "full_name": self.full_name,
            "is_super_admin": self.is_super_admin
        }

    @staticmethod
    def from_db_record(record: dict):
        """
        Static method to create an AdminUser object from a database dictionary record.
        """
        return AdminUser(
            user_id=record.get('user_id'),
            username=record.get('username'),
            password_hash=record.get('password_hash'),
            full_name=record.get('full_name'),
            # Convert database boolean (often 0/1 or False/True) to Python boolean
            is_super_admin=bool(record.get('is_super_admin')) 
        )