from decimal import ROUND_HALF_UP, Decimal
from typing import Optional

from models.attendance import Attendance
from models.salary_structure import SalaryStructure


class SalaryCalculator:

    def __init__(self, working_days_in_month: int = 30):
        self.working_days_in_month = working_days_in_month

    def calculate_salary(
        self,
        basic_salary: Decimal,
        salary_structure: SalaryStructure,
        attendance: Optional[Attendance] = None,
    ) -> dict:

        if basic_salary <= 0:
            raise ValueError("Basic salary must be greater than zero")

        if salary_structure.housing_allowance_pct < 0 or salary_structure.tax_rate_pct < 0:
            raise ValueError("Invalid percentage values")

        # ---------- Attendance Proration ----------
        payable_basic = basic_salary

        if attendance:
            if attendance.days_worked < 0:
                raise ValueError("Invalid attendance")

            payable_basic = (
                basic_salary * Decimal(attendance.days_worked)
                / Decimal(self.working_days_in_month)
            )

        # ---------- Earnings ----------
        hra = payable_basic * salary_structure.housing_allowance_pct

        transport = (
            salary_structure.transport_allowance
            * (payable_basic / basic_salary)
        )

        gross_salary = payable_basic + hra + transport

        # ---------- Deductions ----------
        tax = gross_salary * salary_structure.tax_rate_pct

        net_salary = gross_salary - tax

        if net_salary < 0:
            net_salary = Decimal("0.00")

        # ---------- Rounding ----------
        return {
            "basic_salary": self._round(payable_basic),
            "hra": self._round(hra),
            "transport_allowance": self._round(transport),
            "tax": self._round(tax),
            "gross_salary": self._round(gross_salary),
            "net_salary": self._round(net_salary),
        }

    def _round(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)