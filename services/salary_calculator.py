# services/salary_calculator.py

from decimal import Decimal, ROUND_HALF_UP
from typing import Optional

from models.salary_structure import SalaryStructure
from models.attendance import Attendance


class SalaryCalculator:
    """
    Handles salary calculation logic.
    No database or GUI code here.
    """

    def __init__(self, working_days_in_month: int = 30):
        self.working_days_in_month = working_days_in_month

    # --------------------------------------------------
    # CORE SALARY CALCULATION
    # --------------------------------------------------
    def calculate_salary(
        self,
        basic_salary: Decimal,
        salary_structure: SalaryStructure,
        attendance: Optional[Attendance] = None
    ) -> dict:
        """
        Calculate salary using salary structure and (optional) attendance.

        Returns a dictionary with full salary breakup.
        """

        if basic_salary <= 0:
            raise ValueError("Basic salary must be greater than zero")

        # ---------- Attendance Proration ----------
        payable_basic = basic_salary

        if attendance:
            total_days = attendance.days_worked + attendance.days_absent
            if total_days > 0:
                payable_basic = (
                    basic_salary
                    * Decimal(attendance.days_worked)
                    / Decimal(total_days)
                )

        # ---------- Earnings ----------
        hra = payable_basic * salary_structure.housing_allowance_pct
        transport = salary_structure.transport_allowance

        gross_salary = payable_basic + hra + transport

        # ---------- Deductions ----------
        tax = gross_salary * salary_structure.tax_rate_pct

        net_salary = gross_salary - tax

        # ---------- Rounding ----------
        return {
            "basic_salary": self._round(payable_basic),
            "hra": self._round(hra),
            "transport_allowance": self._round(transport),
            "tax": self._round(tax),
            "gross_salary": self._round(gross_salary),
            "net_salary": self._round(net_salary),
        }

    # --------------------------------------------------
    # UTILITY
    # --------------------------------------------------
    def _round(self, value: Decimal) -> Decimal:
        return value.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
