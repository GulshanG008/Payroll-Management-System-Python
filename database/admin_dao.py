# database/admin_dao.py
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from database.connection import get_db_connection, release_db_connection
# Note: In a real app, you would import a hashing library (like bcrypt or hashlib)
# from models.admin import AdminUser # Assuming this model is ready

class AdminDAO:
    """
    Handles all data access operations related to Admin users.
    """
    def __init__(self):
        # We assume the connection manager has been initialized via its singleton instance.
        self.create_admin_table()

    def create_admin_table(self):
        """Creates the admin_users table if it does not exist."""
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS admin_users (
            user_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(50) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            full_name VARCHAR(100),
            is_super_admin BOOLEAN DEFAULT FALSE
        )
        """
        try:
            cursor.execute(query)
            conn.commit()
            print("Admin table checked/created successfully.")
            self.add_initial_admin(conn) # Attempt to set up a default admin if none exist
        except Error as e:
            print(f"Error creating admin table: {e}")
        finally:
            cursor.close()
            release_db_connection(conn)

    def add_initial_admin(self, conn):
        """Adds a default administrator if the table is empty for first-time use."""
        cursor = conn.cursor()
        
        # Check if any admin exists
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        if cursor.fetchone()[0] == 0:
            # ⚠️ SECURITY WARNING: This is a plain text password for simplicity.
            # In production, use strong hashing (e.g., bcrypt) here!
            initial_password = "admin123" 
            
            insert_query = """
            INSERT INTO admin_users (username, password_hash, full_name, is_super_admin)
            VALUES (%s, %s, %s, %s)
            """
            values = ("admin", initial_password, "System Administrator", True)
            
            try:
                cursor.execute(insert_query, values)
                conn.commit()
                print("Initial default admin user 'admin' added (password: admin123).")
            except Error as e:
                print(f"Error adding initial admin: {e}")
                conn.rollback()
        
        cursor.close()
        # Note: The connection is released in the calling method (create_admin_table)

    def authenticate_admin(self, uid, username, password):
        """
        Authenticates an admin user using user_id, username, and password.
        Returns True on successful login, False otherwise.
        """
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Connection failed during login attempt.")
            return False
            
        cursor = conn.cursor()
        
        # ⚠️ NOTE: This query compares against the stored plain text password (password_hash).
        # In a secure app, you would fetch the hash and use a hashing library to verify.
        query = """
        SELECT password_hash FROM admin_users 
        WHERE user_id = %s AND username = %s
        """
        values = (uid, username)
        
        is_authenticated = False
        try:
            cursor.execute(query, values)
            record = cursor.fetchone()
            
            if record:
                stored_password = record[0]
                # Simple plain text comparison (replace with hash verification in production!)
                if password == stored_password:
                    is_authenticated = True
                else:
                    print("Debug: Password mismatch.")
            else:
                print("Debug: User ID/Username not found.")
                
        except Error as e:
            print(f"Authentication Error: {e}")
            messagebox.showerror("Authentication Error", "A database error occurred during login.")
        finally:
            cursor.close()
            release_db_connection(conn)
            
        return is_authenticated

    def get_admin_user_by_id(self, user_id):
        """Fetches admin user details by ID."""
        # This is an example of another method you would implement
        # to fetch a user's details after successful login.
        pass