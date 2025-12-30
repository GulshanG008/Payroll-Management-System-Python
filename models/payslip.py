# models/payslip.py

from decimal import Decimal


class Payslip:
    def __init__(
        self,
        payroll_id: int,
        emp_id: int,
        month_year: str,
        basic_salary: Decimal,
        hra: Decimal,
        da: Decimal,
        transport_allowance: Decimal,
        pf: Decimal,
        tax: Decimal,
        gross_salary: Decimal,
        net_salary: Decimal,
        pdf_path: str,
    ):
        self.payroll_id = payroll_id
        self.emp_id = emp_id
        self.month_year = month_year
        self.basic_salary = basic_salary
        self.hra = hra
        self.da = da
        self.transport_allowance = transport_allowance
        self.pf = pf
        self.tax = tax
        self.gross_salary = gross_salary
        self.net_salary = net_salary
        self.pdf_path = pdf_path

    def __repr__(self):
        return (
            f"Payslip("
            f"PayrollID={self.payroll_id}, "
            f"EmpID={self.emp_id}, "
            f"Month='{self.month_year}', "
            f"NetSalary={self.net_salary})"
        )

    def to_dict(self):
        return {
            "payroll_id": self.payroll_id,
            "emp_id": self.emp_id,
            "month_year": self.month_year,
            "basic_salary": self.basic_salary,
            "hra": self.hra,
            "da": self.da,
            "transport_allowance": self.transport_allowance,
            "pf": self.pf,
            "tax": self.tax,
            "gross_salary": self.gross_salary,
            "net_salary": self.net_salary,
            "pdf_path": self.pdf_path,
        }

    @staticmethod
    def from_db_record(record: dict):
        if not record:
            return None

        def safe_decimal(value):
            return Decimal(str(value)) if value is not None else Decimal("0.00")

        return Payslip(
            payroll_id=record.get("payroll_id"),
            emp_id=record.get("emp_id"),
            month_year=record.get("month_year"),
            basic_salary=safe_decimal(record.get("basic_salary")),
            hra=safe_decimal(record.get("hra")),
            da=safe_decimal(record.get("da")),
            transport_allowance=safe_decimal(record.get("transport_allowance")),
            pf=safe_decimal(record.get("pf")),
            tax=safe_decimal(record.get("tax")),
            gross_salary=safe_decimal(record.get("gross_salary")),
            net_salary=safe_decimal(record.get("net_salary")),
            pdf_path=record.get("pdf_path"),
        )
