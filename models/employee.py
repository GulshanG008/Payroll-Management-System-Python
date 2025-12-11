# models/employee.py

from datetime import date
from decimal import Decimal

class Employee:
    def __init__(self, id: int, name: str, role: str, salary: Decimal, hire_date: date = None):
        self.id = id
        self.name = name
        self.role = role
        self.salary = salary 
        self.hire_date = hire_date if hire_date is not None else date.today()

    def __repr__(self):
        return f"Employee(ID={self.id}, Name='{self.name}', Role='{self.role}', Salary={self.salary})"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "salary": self.salary,
            "hire_date": self.hire_date
        }

    @staticmethod
    def from_db_record(record: dict):
        salary_value = record.get('salary')
        if not isinstance(salary_value, Decimal):
             try:
                 salary_value = Decimal(str(salary_value))
             except:
                 salary_value = Decimal('0.00') 
        return Employee(
            id=record.get('id'),
            name=record.get('name'),
            role=record.get('role'),
            salary=salary_value,
            hire_date=record.get('hire_date')
        )