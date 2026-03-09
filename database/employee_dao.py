# database/employee_dao.py

from decimal import Decimal
from typing import List, Optional

from database.connection import get_db_connection, get_db_cursor, release_db_connection


class EmployeeDAO:
    # EMPTY TABLE INITTIALIZATION

    # CREATE
    def create_employee(
        self,
        emp_code: str,
        full_name: str,
        gender: str,
        contact_no: str,
        email: str,
        date_of_joining,
        basic_salary: Decimal,
        structure_id: Optional[int] = None,
    ) -> int:
        query = """
            INSERT INTO employee (
                emp_code,
                full_name,
                gender,
                contact_no,
                email,
                date_of_joining,
                basic_salary,
                structure_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(
                query,
                (
                    emp_code,
                    full_name,
                    gender,
                    contact_no,
                    email,
                    date_of_joining,
                    basic_salary,
                    structure_id,
                ),
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            release_db_connection(conn)

    # READ BY ID
    def get_by_id(self, emp_id: int) -> Optional[dict]:
        query = """
            SELECT *
            FROM employee
            WHERE emp_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (emp_id,))
            return cursor.fetchone()
        finally:
            release_db_connection(conn)

    # READ BY EMP CODE
    def get_by_emp_code(self, emp_code: str) -> Optional[dict]:
        query = """
            SELECT *
            FROM employee
            WHERE emp_code = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (emp_code,))
            return cursor.fetchone()
        finally:
            release_db_connection(conn)

    # READ ALL ACTIVE EMPLOYEES
    def get_all_active(self) -> List[dict]:
        query = """
            SELECT *
            FROM employee
            WHERE status = 'ACTIVE'
            ORDER BY full_name
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            release_db_connection(conn)

    # UPDATE
    def update_employee(
        self,
        emp_id: int,
        full_name: str,
        gender: str,
        contact_no: str,
        email: str,
        basic_salary: Decimal,
        structure_id: Optional[int],
    ) -> bool:
        query = """
            UPDATE employee
            SET
                full_name = %s,
                gender = %s,
                contact_no = %s,
                email = %s,
                basic_salary = %s,
                structure_id = %s
            WHERE emp_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(
                query,
                (
                    full_name,
                    gender,
                    contact_no,
                    email,
                    basic_salary,
                    structure_id,
                    emp_id,
                ),
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)

    # DEACTIVATE (SOFT DELETE)
    def deactivate_employee(self, emp_id: int) -> bool:
        query = """
            UPDATE employee
            SET status = 'INACTIVE'
            WHERE emp_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (emp_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)

    # DELETE (HARD DELETE - USE CAREFULLY)
    def delete_employee(self, emp_id: int) -> bool:
        query = """
            DELETE FROM employee
            WHERE emp_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (emp_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)
