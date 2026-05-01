from database.attendance_dao import AttendanceDAO
from models.attendance import Attendance
import re


class AttendanceService:

    def __init__(self):
        self.attendance_dao = AttendanceDAO()

    def _validate(self, month_year: str, days_worked: int, days_absent: int):

        if not month_year:
            raise ValueError("Month is required")

        # Example format: "01-2025"
        if not re.match(r"^\d{2}-\d{4}$", month_year):
            raise ValueError("Invalid month format (MM-YYYY expected)")

        if days_worked < 0 or days_absent < 0:
            raise ValueError("Days cannot be negative")

        total_days = days_worked + days_absent

        if total_days == 0:
            raise ValueError("Invalid attendance data")

        if total_days > 31:
            raise ValueError("Total days exceed possible limit")

    def record_attendance(
        self, emp_id: int, month_year: str, days_worked: int, days_absent: int
    ) -> Attendance:

        self._validate(month_year, days_worked, days_absent)

        try:
            existing = self.attendance_dao.get_by_employee_and_month(emp_id, month_year)
        except Exception as e:
            raise Exception(f"Database error: {e}")

        if existing:
            raise ValueError("Attendance already exists for this month")

        attendance_id = self.attendance_dao.add_attendance(
            emp_id, month_year, days_worked, days_absent
        )

        return Attendance(
            attendance_id=attendance_id,
            emp_id=emp_id,
            month_year=month_year,
            days_worked=days_worked,
            days_absent=days_absent,
        )

    def get_attendance(self, emp_id: int, month_year: str) -> Attendance | None:
        record = self.attendance_dao.get_by_employee_and_month(emp_id, month_year)
        return Attendance.from_db_record(record) if record else None

    def list_attendance_for_employee(self, emp_id: int):
        records = self.attendance_dao.get_all_for_employee(emp_id)
        return [Attendance.from_db_record(r) for r in records]

    def update_attendance(
        self, attendance_id: int, days_worked: int, days_absent: int
    ) -> bool:

        self._validate("01-2000", days_worked, days_absent)  # reuse validation

        return self.attendance_dao.update_attendance(
            attendance_id, days_worked, days_absent
        )

    def delete_attendance(self, attendance_id: int) -> bool:

        deleted = self.attendance_dao.delete_attendance(attendance_id)

        if not deleted:
            raise ValueError("Record not found or already deleted")

        return deleted