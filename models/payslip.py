from decimal import Decimal


class Payslip:

    def __init__(
        self,
        payroll_id: int,
        emp_id: int,
        month: int,
        year: int,
        basic_salary: Decimal,
        hra: Decimal,
        da: Decimal,
        transport_allowance: Decimal,
        pf: Decimal,
        tax: Decimal,
        gross_salary: Decimal,
        net_salary: Decimal,
        pdf_path: str = None,
    ):

        if month < 1 or month > 12:
            raise ValueError("Invalid month")

        if year < 2000:
            raise ValueError("Invalid year")

        if net_salary < 0:
            raise ValueError("Invalid net salary")

        self.payroll_id = payroll_id
        self.emp_id = emp_id
        self.month = month
        self.year = year
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
            f"ID={self.payroll_id}, "
            f"EmpID={self.emp_id}, "
            f"Month={self.month}/{self.year}, "
            f"NetSalary={self.net_salary})"
        )

    def to_dict(self):
        return {
            "payroll_id": self.payroll_id,
            "emp_id": self.emp_id,
            "month": self.month,
            "year": self.year,
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
            payroll_id=record["payroll_id"],
            emp_id=record["emp_id"],
            month=record["month"],
            year=record["year"],
            basic_salary=safe_decimal(record["basic_salary"]),
            hra=safe_decimal(record["hra"]),
            da=safe_decimal(record["da"]),
            transport_allowance=safe_decimal(record["transport_allowance"]),
            pf=safe_decimal(record["pf"]),
            tax=safe_decimal(record["tax"]),
            gross_salary=safe_decimal(record["gross_salary"]),
            net_salary=safe_decimal(record["net_salary"]),
            pdf_path=record.get("pdf_path"),
        )