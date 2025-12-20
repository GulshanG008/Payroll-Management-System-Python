# services/payroll_service.py

import os
from reports.pdf_generator import generate_payslip_pdf


class PayrollService:
    def __init__(self, db=None):
        self.db = db

    def generate_payroll(self, salary_month):
        if not salary_month:
            raise ValueError("Salary month is required")

        # ---- SAMPLE DATA (replace with DB later) ----
        emp_id = "EMP001"
        emp_name = "Rahul Kumar"

        basic = 20000
        hra = 8000
        da = 4000
        pf = 2000
        tax = 1500

        gross_salary = basic + hra + da
        net_salary = gross_salary - (pf + tax)

        # ---- FILE PATH ----
        output_dir = os.path.join("reports", "payslip")
        os.makedirs(output_dir, exist_ok=True)

        file_name = f"Payslip_{emp_id}_{salary_month}.pdf"
        file_path = os.path.join(output_dir, file_name)

        # ---- PDF GENERATION ----
        generate_payslip_pdf(
            file_path=file_path,
            emp_id=emp_id,
            emp_name=emp_name,
            salary_month=salary_month,
            basic_salary=basic,
            hra=hra,
            da=da,
            pf=pf,
            tax=tax,
            gross_salary=gross_salary,
            net_salary=net_salary
        )

        return {
            "status": "success",
            "message": f"Payslip generated successfully.\nSaved in reports/payslip",
            "file_path": file_path
        }
