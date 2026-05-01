from database.connection import execute_query


class AttendanceDAO:

    def add_attendance(self, emp_id: int, month_year: str,
                       days_worked: int, days_absent: int) -> int:

        if days_worked < 0 or days_absent < 0:
            raise ValueError("Days cannot be negative")

        query = """
            INSERT INTO attendance (
                emp_id, month_year, days_worked, days_absent
            )
            VALUES (%s, %s, %s, %s)
        """

        return execute_query(query, (emp_id, month_year, days_worked, days_absent))


    def get_by_employee_and_month(self, emp_id: int, month_year: str):
        query = """
            SELECT *
            FROM attendance
            WHERE emp_id = %s AND month_year = %s
        """
        return execute_query(query, (emp_id, month_year), fetch_one=True)


    def update_attendance(self, attendance_id: int,
                          days_worked: int, days_absent: int) -> bool:

        if days_worked < 0 or days_absent < 0:
            raise ValueError("Days cannot be negative")

        query = """
            UPDATE attendance
            SET days_worked = %s, days_absent = %s
            WHERE attendance_id = %s
        """

        result = execute_query(query, (days_worked, days_absent, attendance_id))
        return result is not None


    def delete_attendance(self, attendance_id: int) -> bool:
        query = """
            DELETE FROM attendance
            WHERE attendance_id = %s
        """

        result = execute_query(query, (attendance_id,))
        return result is not None


    def get_all_for_employee(self, emp_id: int):
        query = """
            SELECT *
            FROM attendance
            WHERE emp_id = %s
            ORDER BY month_year DESC
        """
        return execute_query(query, (emp_id,), fetch_all=True)