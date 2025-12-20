# database/payslip_dao.py

from typing import Optional, List
from decimal import Decimal

from database.connection import (
    get_db_connection,
    get_db_cursor,
    release_db_connection
)


class PayslipDAO:
    """
    Data Access Object for Payroll / Payslip table.
    Stores generated salary details and PDF path.
    """

    # --------------------------------------------------
    # CREATE PAYSLIP
    # --------------------------------------------------
    def create_payslip(
        self,
        emp_id: int,
        month_year: str,
        basic_salary: Decimal,
        hra: Decimal,
        da: Decimal,
        transport_allowance: Decimal,
        pf: Decimal,
        tax: Decimal,
        gross_salary: Decimal,
        net_salary: Decimal,
        pdf_path: str
    ) -> int:
        query = """
            INSERT INTO payroll (
                emp_id,
                month_year,
                basic_salary,
                hra,
                da,
                transport_allowance,
                pf,
                tax,
                gross_salary,
                net_salary,
                pdf_path
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(
                query,
                (
                    emp_id,
                    month_year,
                    basic_salary,
                    hra,
                    da,
                    transport_allowance,
                    pf,
                    tax,
                    gross_salary,
                    net_salary,
                    pdf_path
                )
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # READ BY EMPLOYEE & MONTH
    # --------------------------------------------------
    def get_by_employee_and_month(
        self,
        emp_id: int,
        month_year: str
    ) -> Optional[dict]:
        query = """
            SELECT *
            FROM payroll
            WHERE emp_id = %s AND month_year = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (emp_id, month_year))
            return cursor.fetchone()
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # READ ALL PAYSLIPS FOR EMPLOYEE
    # --------------------------------------------------
    def get_all_for_employee(self, emp_id: int) -> List[dict]:
        query = """
            SELECT *
            FROM payroll
            WHERE emp_id = %s
            ORDER BY generated_at DESC
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (emp_id,))
            return cursor.fetchall()
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # READ ALL PAYSLIPS (ADMIN)
    # --------------------------------------------------
    def get_all(self) -> List[dict]:
        query = """
            SELECT p.*, e.emp_code, e.full_name
            FROM payroll p
            JOIN employee e ON p.emp_id = e.emp_id
            ORDER BY p.generated_at DESC
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query)
            return cursor.fetchall()
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # DELETE PAYSLIP
    # --------------------------------------------------
    def delete_payslip(self, payroll_id: int) -> bool:
        query = """
            DELETE FROM payroll
            WHERE payroll_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (payroll_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)
