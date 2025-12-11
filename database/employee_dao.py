# database/employee_dao.py

import mysql.connector
from mysql.connector import Error
from database.connection import get_db_connection, release_db_connection
from tkinter import messagebox # Used for showing database errors to the user

class EmployeeDAO:
    def __init__(self):
        self.create_employee_table()

    def create_employee_table(self):
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS employees (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            role VARCHAR(100),
            salary DECIMAL(10, 2) NOT NULL,
            hire_date DATE
        )
        """
        try:
            cursor.execute(query)
            conn.commit()
            print("Employees table checked/created successfully.")
        except Error as e:
            print(f"Error creating employees table: {e}")
            messagebox.showerror("DB Setup Error", f"Could not create employees table: {e}")
        finally:
            cursor.close()
            release_db_connection(conn)

    def get_all_employees(self):
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor(dictionary=True) 
        query = "SELECT id, name, role, salary, hire_date FROM employees ORDER BY id"
        employees = []
        
        try:
            cursor.execute(query)
            employees = cursor.fetchall()
        except Error as e:
            print(f"Error fetching employees: {e}")
            messagebox.showerror("DB Read Error", "Failed to retrieve employee list.")
        finally:
            cursor.close()
            release_db_connection(conn)
            
        return employees

    def add_employee(self, name, role, salary, hire_date=None):
        conn = get_db_connection()
        if not conn:
            return None

        cursor = conn.cursor()
        query = "INSERT INTO employees (name, role, salary, hire_date) VALUES (%s, %s, %s, %s)"
        values = (name, role, salary, hire_date if hire_date else mysql.connector.Date.today())
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid 
        except Error as e:
            print(f"Error adding employee: {e}")
            messagebox.showerror("DB Write Error", f"Failed to add employee: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            release_db_connection(conn)

    def update_employee(self, employee_id, name, role, salary, hire_date):
        conn = get_db_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        query = "UPDATE employees SET name = %s, role = %s, salary = %s, hire_date = %s WHERE id = %s"
        values = (name, role, salary, hire_date, employee_id)
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0 
        except Error as e:
            print(f"Error updating employee: {e}")
            messagebox.showerror("DB Update Error", f"Failed to update employee: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            release_db_connection(conn)

    def delete_employee(self, employee_id):
        conn = get_db_connection()
        if not conn:
            return False

        cursor = conn.cursor()
        query = "DELETE FROM employees WHERE id = %s"
        
        try:
            cursor.execute(query, (employee_id,))
            conn.commit()
            return cursor.rowcount > 0 
        except Error as e:
            print(f"Error deleting employee: {e}")
            messagebox.showerror("DB Delete Error", f"Failed to delete employee: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            release_db_connection(conn)