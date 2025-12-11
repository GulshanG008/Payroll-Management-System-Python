# models/employee.py

from datetime import date
from decimal import Decimal

class Employee:
    """
    Data model for an Employee record. 
    This class represents a single row from the 'employees' database table 
    and is used consistently across the GUI, Services, and DAO layers.
    """
    def __init__(self, id: int, name: str, role: str, salary: Decimal, hire_date: date = None):
        self.id = id
        self.name = name
        self.role = role
        # Ensure salary is stored as a Decimal for financial precision
        self.salary = salary 
        # hire_date defaults to today if not provided, though DAO typically handles this
        self.hire_date = hire_date if hire_date is not None else date.today()

    def __repr__(self):
        """Provides a helpful string representation for debugging."""
        return f"Employee(ID={self.id}, Name='{self.name}', Role='{self.role}', Salary={self.salary})"

    def to_dict(self):
        """
        Converts the Employee object into a dictionary.
        Useful for passing data to GUI components or serialization.
        """
        return {
            "id": self.id,
            "name": self.name,
            "role": self.role,
            "salary": self.salary,
            "hire_date": self.hire_date
        }

    @staticmethod
    def from_db_record(record: dict):
        """
        Static method to create an Employee object from a dictionary record 
        (typically fetched by the EmployeeDAO with dictionary=True).
        """
        # Ensure salary is converted to Decimal if it's not already (e.g., if coming from raw string input)
        salary_value = record.get('salary')
        if not isinstance(salary_value, Decimal):
             try:
                 salary_value = Decimal(str(salary_value))
             except:
                 salary_value = Decimal('0.00') # Default safety fallback
                 
        return Employee(
            id=record.get('id'),
            name=record.get('name'),
            role=record.get('role'),
            salary=salary_value,
            hire_date=record.get('hire_date')
        )