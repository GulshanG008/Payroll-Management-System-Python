<<<<<<< HEAD
=======
# database/attendance_dao.py

from database.connection import (
    get_db_connection,
    get_db_cursor,
    release_db_connection
)


class AttendanceDAO:
    """
    Data Access Object for Attendance table.
    """

    # --------------------------------------------------
    # CREATE / ADD ATTENDANCE
    # --------------------------------------------------
    def add_attendance(
        self,
        emp_id: int,
        month_year: str,
        days_worked: int,
        days_absent: int
    ) -> int:
        query = """
            INSERT INTO attendance (
                emp_id,
                month_year,
                days_worked,
                days_absent
            )
            VALUES (%s, %s, %s, %s)
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(
                query,
                (emp_id, month_year, days_worked, days_absent)
            )
            conn.commit()
            return cursor.lastrowid
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # READ BY EMPLOYEE + MONTH
    # --------------------------------------------------
    def get_by_employee_and_month(
        self,
        emp_id: int,
        month_year: str
    ):
        query = """
            SELECT *
            FROM attendance
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
    # UPDATE ATTENDANCE
    # --------------------------------------------------
    def update_attendance(
        self,
        attendance_id: int,
        days_worked: int,
        days_absent: int
    ) -> bool:
        query = """
            UPDATE attendance
            SET
                days_worked = %s,
                days_absent = %s
            WHERE attendance_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(
                query,
                (days_worked, days_absent, attendance_id)
            )
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # DELETE ATTENDANCE
    # --------------------------------------------------
    def delete_attendance(self, attendance_id: int) -> bool:
        query = """
            DELETE FROM attendance
            WHERE attendance_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (attendance_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # LIST ALL ATTENDANCE FOR EMPLOYEE
    # --------------------------------------------------
    def get_all_for_employee(self, emp_id: int):
        query = """
            SELECT *
            FROM attendance
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
>>>>>>> backend
