def calculate_salary(
    self,
    basic_salary: Decimal,
    salary_structure: SalaryStructure,
    attendance: Optional[Attendance] = None,
) -> dict:

    if basic_salary <= 0:
        raise ValueError("Basic salary must be greater than zero")

    # ---------- Validation ----------
    for pct in [
        salary_structure.housing_allowance_pct,
        salary_structure.tax_rate_pct,
        salary_structure.da_pct,
        salary_structure.pf_pct,
    ]:
        if not (Decimal("0") <= pct <= Decimal("1")):
            raise ValueError("Invalid percentage value")

    # ---------- Attendance ----------
    payable_basic = basic_salary

    if attendance:
        total_days = attendance.days_worked + attendance.days_absent

        if total_days <= 0 or total_days > self.working_days_in_month:
            raise ValueError("Invalid attendance data")

        payable_basic = (
            basic_salary * Decimal(attendance.days_worked)
            / Decimal(self.working_days_in_month)
        )

    # ---------- Earnings ----------
    hra = payable_basic * salary_structure.housing_allowance_pct
    da = payable_basic * salary_structure.da_pct

    transport = salary_structure.transport_allowance * (
        payable_basic / basic_salary
    )

    gross_salary = payable_basic + hra + da + transport

    # ---------- Deductions ----------
    pf = gross_salary * salary_structure.pf_pct
    tax = gross_salary * salary_structure.tax_rate_pct

    total_deductions = pf + tax

    net_salary = gross_salary - total_deductions

    if net_salary < 0:
        net_salary = Decimal("0.00")

    # ---------- Output ----------
    return {
        "basic_salary": self._round(payable_basic),
        "hra": self._round(hra),
        "da": self._round(da),
        "transport_allowance": self._round(transport),
        "pf": self._round(pf),
        "tax": self._round(tax),
        "gross_salary": self._round(gross_salary),
        "net_salary": self._round(net_salary),
    }