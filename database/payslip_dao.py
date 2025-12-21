# database/payslip_dao.py

from database.connection import (
    get_db_connection,
    get_db_cursor,
    release_db_connection
)


class PayslipDAO:
    """
    Data Access Object for Payroll / Payslip table.
    """

    # --------------------------------------------------
    # CREATE PAYSLIP / PAYROLL
    # --------------------------------------------------
    def create_payslip(
        self,
        emp_id: int,
        month_year: str,
        basic_salary,
        hra,
        transport_allowance,
        tax,
        gross_salary,
        net_salary
    ) -> int:
        query = """
            INSERT INTO payroll (
                emp_id,
                month_year,
                basic_salary,
                hra,
                transport_allowance,
                tax,
                gross_salary,
                net_salary
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
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
                    transport_allowance,
                    tax,
                    gross_salary,
                    net_salary
                )
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # UPDATE PDF PATH
    # --------------------------------------------------
    def update_pdf_path(self, payroll_id: int, pdf_path: str) -> bool:
        query = """
            UPDATE payroll
            SET pdf_path = %s
            WHERE payroll_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (pdf_path, payroll_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # GET PAYSLIP BY EMPLOYEE + MONTH
    # --------------------------------------------------
    def get_by_employee_and_month(
        self,
        emp_id: int,
        month_year: str
    ):
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
    # LIST PAYSLIPS FOR EMPLOYEE
    # --------------------------------------------------
    def get_all_for_employee(self, emp_id: int):
        query = """
            SELECT *
            FROM payroll
            WHERE emp_id = %s
            ORDER BY month_year DESC
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (emp_id,))
            return cursor.fetchall()
        finally:
            release_db_connection(conn)
