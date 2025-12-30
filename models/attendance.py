# models/attendance.py


class Attendance:
    def __init__(
        self,
        attendance_id: int,
        emp_id: int,
        month_year: str,
        days_worked: int,
        days_absent: int,
    ):
        self.attendance_id = attendance_id
        self.emp_id = emp_id
        self.month_year = month_year
        self.days_worked = days_worked
        self.days_absent = days_absent

    def __repr__(self):
        return (
            f"Attendance("
            f"ID={self.attendance_id}, "
            f"EmpID={self.emp_id}, "
            f"Month='{self.month_year}', "
            f"Worked={self.days_worked}, "
            f"Absent={self.days_absent})"
        )

    def to_dict(self):
        return {
            "attendance_id": self.attendance_id,
            "emp_id": self.emp_id,
            "month_year": self.month_year,
            "days_worked": self.days_worked,
            "days_absent": self.days_absent,
        }

    @staticmethod
    def from_db_record(record: dict):
        if not record:
            return None

        return Attendance(
            attendance_id=record.get("attendance_id"),
            emp_id=record.get("emp_id"),
            month_year=record.get("month_year"),
            days_worked=record.get("days_worked"),
            days_absent=record.get("days_absent"),
        )
