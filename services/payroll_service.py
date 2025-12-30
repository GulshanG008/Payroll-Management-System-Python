# services/payroll_service.py

from decimal import Decimal

from database.attendance_dao import AttendanceDAO
from database.employee_dao import EmployeeDAO
from database.payslip_dao import PayslipDAO
from database.salary_dao import SalaryDAO
from reports.pdf_generator import generate_payslip_pdf
from services.salary_calculator import SalaryCalculator


class PayrollService:
    def __init__(self):
        self.employee_dao = EmployeeDAO()
        self.salary_dao = SalaryDAO()
        self.attendance_dao = AttendanceDAO()
        self.payslip_dao = PayslipDAO()

        self.calculator = SalaryCalculator()

    def generate_payroll(self, emp_id: int, month_year: str) -> int:
        # 1️⃣ Get employee
        employee = self.employee_dao.get_by_id(emp_id)
        if not employee:
            raise ValueError("Employee not found")

        # 2️⃣ Get salary structure
        structure = None
        if employee["structure_id"]:
            structure = self.salary_dao.get_by_id(employee["structure_id"])

        if not structure:
            raise ValueError("Salary structure not assigned")

        # 3️⃣ Get attendance (optional)
        attendance_record = self.attendance_dao.get_by_employee_and_month(
            emp_id, month_year
        )

        # 4️⃣ Calculate salary
        salary_data = self.calculator.calculate_salary(
            basic_salary=Decimal(employee["basic_salary"]),
            salary_structure=structure,
            attendance=(None if not attendance_record else attendance_record),
        )

        # 5️⃣ Save payroll record
        payroll_id = self.payslip_dao.create_payslip(
            emp_id=emp_id, month_year=month_year, **salary_data
        )

        # 6️⃣ Generate PDF
        pdf_path = generate_payslip_pdf(
            employee=employee, month_year=month_year, salary_data=salary_data
        )

        # 7️⃣ Update PDF path
        self.payslip_dao.update_pdf_path(payroll_id, pdf_path)

        return payroll_id
