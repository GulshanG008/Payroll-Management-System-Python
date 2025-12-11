# database/admin_dao.py
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from database.connection import get_db_connection, release_db_connection

class AdminDAO:
    def __init__(self):
        self.create_admin_table()

    def create_admin_table(self):
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
            self.add_initial_admin(conn) 
        except Error as e:
            print(f"Error creating admin table: {e}")
        finally:
            cursor.close()
            release_db_connection(conn)

    def add_initial_admin(self, conn):
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM admin_users")
        if cursor.fetchone()[0] == 0:
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

    def authenticate_admin(self, uid, username, password):
        conn = get_db_connection()
        if not conn:
            messagebox.showerror("Database Error", "Connection failed during login attempt.")
            return False
            
        cursor = conn.cursor()

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
        pass