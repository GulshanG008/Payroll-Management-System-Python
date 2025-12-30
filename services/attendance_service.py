# services/attendance_service.py

from database.attendance_dao import AttendanceDAO
from models.attendance import Attendance


class AttendanceService:
    def __init__(self):
        self.attendance_dao = AttendanceDAO()

    # ADD / RECORD ATTENDANCE
    def record_attendance(
        self, emp_id: int, month_year: str, days_worked: int, days_absent: int
    ) -> Attendance:
        if not month_year:
            raise ValueError("Month is required")

        if days_worked < 0 or days_absent < 0:
            raise ValueError("Attendance days cannot be negative")

        attendance_id = self.attendance_dao.add_attendance(
            emp_id=emp_id,
            month_year=month_year,
            days_worked=days_worked,
            days_absent=days_absent,
        )

        return Attendance(
            attendance_id=attendance_id,
            emp_id=emp_id,
            month_year=month_year,
            days_worked=days_worked,
            days_absent=days_absent,
        )

    # GET ATTENDANCE FOR EMPLOYEE & MONTH
    def get_attendance(self, emp_id: int, month_year: str) -> Attendance | None:
        record = self.attendance_dao.get_by_employee_and_month(emp_id, month_year)

        if not record:
            return None

        return Attendance.from_db_record(record)

    # UPDATE ATTENDANCE
    def update_attendance(
        self, attendance_id: int, days_worked: int, days_absent: int
    ) -> bool:
        if days_worked < 0 or days_absent < 0:
            raise ValueError("Attendance days cannot be negative")

        return self.attendance_dao.update_attendance(
            attendance_id=attendance_id,
            days_worked=days_worked,
            days_absent=days_absent,
        )

    # DELETE ATTENDANCE RECORD
    def delete_attendance(self, attendance_id: int) -> bool:
        return self.attendance_dao.delete_attendance(attendance_id)

    # LIST ATTENDANCE FOR EMPLOYEE
    def list_attendance_for_employee(self, emp_id: int):
        records = self.attendance_dao.get_all_for_employee(emp_id)
        return [Attendance.from_db_record(r) for r in records]
