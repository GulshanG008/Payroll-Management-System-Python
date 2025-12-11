# database/salary_dao.py

import mysql.connector
from mysql.connector import Error
from database.connection import get_db_connection, release_db_connection
from models.salary_structure import SalaryStructure
from decimal import Decimal
from tkinter import messagebox

class SalaryDAO:
    """
    Handles data access operations for SalaryStructure records.
    """
    def __init__(self):
        self.create_salary_structure_table()

    def create_salary_structure_table(self):
        """Creates the salary_structures table if it does not exist."""
        conn = get_db_connection()
        if not conn:
            return

        cursor = conn.cursor()
        query = """
        CREATE TABLE IF NOT EXISTS salary_structures (
            structure_id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL UNIQUE,
            base_salary_min DECIMAL(10, 2) NOT NULL,
            base_salary_max DECIMAL(10, 2) NOT NULL,
            housing_allowance_pct DECIMAL(5, 4) NOT NULL,
            transport_allowance DECIMAL(10, 2) NOT NULL,
            tax_rate_pct DECIMAL(5, 4) NOT NULL
        )
        """
        try:
            cursor.execute(query)
            conn.commit()
            print("Salary structures table checked/created successfully.")
        except Error as e:
            print(f"Error creating salary structures table: {e}")
            messagebox.showerror("DB Setup Error", f"Could not create salary structures table: {e}")
        finally:
            cursor.close()
            release_db_connection(conn)

    # --- R: READ Operations ---

    def get_all_structures(self):
        """Retrieves all salary structure records and returns them as SalaryStructure objects."""
        conn = get_db_connection()
        if not conn:
            return []
            
        cursor = conn.cursor(dictionary=True) 
        query = "SELECT * FROM salary_structures ORDER BY structure_id"
        structures = []
        
        try:
            cursor.execute(query)
            # Convert raw database dicts into model objects
            structures = [SalaryStructure.from_db_record(rec) for rec in cursor.fetchall()]
        except Error as e:
            print(f"Error fetching salary structures: {e}")
            messagebox.showerror("DB Read Error", "Failed to retrieve salary structures list.")
        finally:
            cursor.close()
            release_db_connection(conn)
            
        return structures

    def get_structure_by_id(self, structure_id: int) -> SalaryStructure | None:
        """Retrieves a single salary structure by its ID."""
        conn = get_db_connection()
        if not conn:
            return None
            
        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM salary_structures WHERE structure_id = %s"
        
        try:
            cursor.execute(query, (structure_id,))
            record = cursor.fetchone()
            if record:
                return SalaryStructure.from_db_record(record)
            return None
        except Error as e:
            print(f"Error fetching salary structure ID {structure_id}: {e}")
            return None
        finally:
            cursor.close()
            release_db_connection(conn)

    # --- C, U, D Operations (Skeletal) ---

    def add_structure(self, structure: SalaryStructure) -> int | None:
        """Inserts a new salary structure record."""
        conn = get_db_connection()
        if not conn: return None

        cursor = conn.cursor()
        query = """INSERT INTO salary_structures (name, base_salary_min, base_salary_max, 
                   housing_allowance_pct, transport_allowance, tax_rate_pct) 
                   VALUES (%s, %s, %s, %s, %s, %s)"""
        values = (structure.name, structure.base_salary_min, structure.base_salary_max,
                  structure.housing_allowance_pct, structure.transport_allowance, structure.tax_rate_pct)
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error adding structure: {e}")
            messagebox.showerror("DB Write Error", f"Failed to add salary structure: {e}")
            conn.rollback()
            return None
        finally:
            cursor.close()
            release_db_connection(conn)

    def update_structure(self, structure: SalaryStructure) -> bool:
        """Updates an existing salary structure record."""
        conn = get_db_connection()
        if not conn: return False

        cursor = conn.cursor()
        query = """UPDATE salary_structures SET name = %s, base_salary_min = %s, 
                   base_salary_max = %s, housing_allowance_pct = %s, 
                   transport_allowance = %s, tax_rate_pct = %s WHERE structure_id = %s"""
        values = (structure.name, structure.base_salary_min, structure.base_salary_max,
                  structure.housing_allowance_pct, structure.transport_allowance, 
                  structure.tax_rate_pct, structure.structure_id)
        
        try:
            cursor.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error updating structure: {e}")
            messagebox.showerror("DB Update Error", f"Failed to update structure: {e}")
            conn.rollback()
            return False
        finally:
            cursor.close()
            release_db_connection(conn)

    def delete_structure(self, structure_id: int) -> bool:
        """Deletes a salary structure record by ID."""
        conn = get_db_connection()
        if not conn: return False

        cursor = conn.cursor()
        query = "DELETE FROM salary_structures WHERE structure_id = %s"
        
        try:
            cursor.execute(query, (structure_id,))
            conn.commit()
            return cursor.rowcount > 0
        except Error as e:
            print(f"Error deleting structure ID {structure_id}: {e}")
            messagebox.showerror("DB Delete Error", "Failed to delete salary structure.")
            conn.rollback()
            return False
        finally:
            cursor.close()
            release_db_connection(conn)