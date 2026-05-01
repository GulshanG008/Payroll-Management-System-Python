from decimal import Decimal
from typing import List, Optional

from database.connection import execute_query


class EmployeeDAO:

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

        if basic_salary < 0:
            raise ValueError("Salary cannot be negative")

        query = """
            INSERT INTO employee (
                emp_code, full_name, gender, contact_no,
                email, date_of_joining, basic_salary, structure_id
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        return execute_query(
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

    def get_by_id(self, emp_id: int) -> Optional[dict]:
        query = "SELECT * FROM employee WHERE emp_id = %s"
        return execute_query(query, (emp_id,), fetch_one=True)

    def get_by_emp_code(self, emp_code: str) -> Optional[dict]:
        query = "SELECT * FROM employee WHERE emp_code = %s"
        return execute_query(query, (emp_code,), fetch_one=True)

    def get_all_active(self) -> List[dict]:
        query = """
            SELECT *
            FROM employee
            WHERE status = 'ACTIVE'
            ORDER BY emp_id
        """
        return execute_query(query, fetch_all=True)

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

        if basic_salary < 0:
            raise ValueError("Salary cannot be negative")

        query = """
            UPDATE employee
            SET full_name=%s, gender=%s, contact_no=%s,
                email=%s, basic_salary=%s, structure_id=%s
            WHERE emp_id = %s
        """

        result = execute_query(
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

        return result is not None

    def deactivate_employee(self, emp_id: int) -> bool:
        query = """
            UPDATE employee
            SET status = 'INACTIVE'
            WHERE emp_id = %s
        """
        result = execute_query(query, (emp_id,))
        return result is not None

    def delete_employee(self, emp_id: int) -> bool:
        query = "DELETE FROM employee WHERE emp_id = %s"
        result = execute_query(query, (emp_id,))
        return result is not None