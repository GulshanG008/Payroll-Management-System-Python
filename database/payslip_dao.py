from database.connection import execute_query


class PayslipDAO:

    def create_payslip(
        self,
        emp_id: int,
        month_year: str,
        basic_salary,
        hra,
        transport_allowance,
        tax,
        gross_salary,
        net_salary,
    ) -> int:

        if net_salary < 0:
            raise ValueError("Net salary cannot be negative")

        query = """
            INSERT INTO payroll (
                emp_id, month_year, basic_salary, hra,
                transport_allowance, tax, gross_salary, net_salary
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        return execute_query(
            query,
            (
                emp_id,
                month_year,
                basic_salary,
                hra,
                transport_allowance,
                tax,
                gross_salary,
                net_salary,
            ),
        )

    def update_pdf_path(self, payroll_id: int, pdf_path: str) -> bool:
        query = """
            UPDATE payroll
            SET pdf_path = %s
            WHERE payroll_id = %s
        """

        result = execute_query(query, (pdf_path, payroll_id))
        return result is not None

    def get_by_employee_and_month(self, emp_id: int, month_year: str):
        query = """
            SELECT *
            FROM payroll
            WHERE emp_id = %s AND month_year = %s
        """
        return execute_query(query, (emp_id, month_year), fetch_one=True)

    def get_all_for_employee(self, emp_id: int):
        query = """
            SELECT *
            FROM payroll
            WHERE emp_id = %s
            ORDER BY month_year DESC
        """
        return execute_query(query, (emp_id,), fetch_all=True)