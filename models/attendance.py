class Attendance:

    def __init__(
        self,
        attendance_id: int,
        emp_id: int,
        month: int,
        year: int,
        days_worked: int,
        days_absent: int,
    ):

        if month < 1 or month > 12:
            raise ValueError("Invalid month")

        if year < 2000:
            raise ValueError("Invalid year")

        if days_worked < 0 or days_absent < 0:
            raise ValueError("Days cannot be negative")

        total_days = days_worked + days_absent

        if total_days == 0:
            raise ValueError("Invalid attendance data")

        if total_days > 31:
            raise ValueError("Total days exceed possible limit")

        self.attendance_id = attendance_id
        self.emp_id = emp_id
        self.month = month
        self.year = year
        self.days_worked = days_worked
        self.days_absent = days_absent

    def __repr__(self):
        return (
            f"Attendance("
            f"ID={self.attendance_id}, "
            f"EmpID={self.emp_id}, "
            f"Month={self.month}, "
            f"Year={self.year}, "
            f"Worked={self.days_worked}, "
            f"Absent={self.days_absent})"
        )

    def to_dict(self):
        return {
            "attendance_id": self.attendance_id,
            "emp_id": self.emp_id,
            "month": self.month,
            "year": self.year,
            "days_worked": self.days_worked,
            "days_absent": self.days_absent,
        }

    def total_days(self) -> int:
        return self.days_worked + self.days_absent

    @staticmethod
    def from_db_record(record: dict):
        if not record:
            return None

        return Attendance(
            attendance_id=record["attendance_id"],
            emp_id=record["emp_id"],
            month=record["month"],
            year=record["year"],
            days_worked=record["days_worked"],
            days_absent=record["days_absent"],
        )