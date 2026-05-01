from datetime import date
from decimal import Decimal


class Employee:

    def __init__(
        self,
        emp_id: int,
        emp_code: str,
        full_name: str,
        gender: str,
        contact_no: str,
        email: str,
        basic_salary: Decimal,
        structure_id: int = None,
        status: str = "ACTIVE",
        hire_date: date = None,
    ):

        if not full_name:
            raise ValueError("Employee name required")

        if basic_salary < 0:
            raise ValueError("Salary cannot be negative")

        self.emp_id = emp_id
        self.emp_code = emp_code
        self.full_name = full_name
        self.gender = gender
        self.contact_no = contact_no
        self.email = email
        self.basic_salary = basic_salary
        self.structure_id = structure_id
        self.status = status
        self.hire_date = hire_date if hire_date else date.today()

    def __repr__(self):
        return (
            f"Employee("
            f"ID={self.emp_id}, "
            f"Code='{self.emp_code}', "
            f"Name='{self.full_name}', "
            f"Salary={self.basic_salary})"
        )

    def to_dict(self):
        return {
            "emp_id": self.emp_id,
            "emp_code": self.emp_code,
            "full_name": self.full_name,
            "gender": self.gender,
            "contact_no": self.contact_no,
            "email": self.email,
            "basic_salary": self.basic_salary,
            "structure_id": self.structure_id,
            "status": self.status,
            "hire_date": self.hire_date,
        }

    @staticmethod
    def from_db_record(record: dict):
        if not record:
            return None

        try:
            salary = Decimal(str(record["basic_salary"]))
        except Exception:
            raise ValueError("Invalid salary value from DB")

        return Employee(
            emp_id=record["emp_id"],
            emp_code=record["emp_code"],
            full_name=record["full_name"],
            gender=record["gender"],
            contact_no=record["contact_no"],
            email=record["email"],
            basic_salary=salary,
            structure_id=record.get("structure_id"),
            status=record.get("status", "ACTIVE"),
            hire_date=record.get("date_of_joining"),
        )