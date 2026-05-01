from decimal import Decimal


class SalaryStructure:

    def __init__(
        self,
        structure_id: int,
        name: str,
        base_salary_min: Decimal,
        base_salary_max: Decimal,
        housing_allowance_pct: Decimal = Decimal("0.0"),
        transport_allowance: Decimal = Decimal("0.0"),
        tax_rate_pct: Decimal = Decimal("0.0"),
        da_pct: Decimal = Decimal("0.0"),
        pf_pct: Decimal = Decimal("0.0"),
    ):

        if not name:
            raise ValueError("Structure name required")

        if base_salary_min < 0 or base_salary_max < 0:
            raise ValueError("Salary values cannot be negative")

        if base_salary_min > base_salary_max:
            raise ValueError("Minimum salary cannot exceed maximum salary")

        if transport_allowance < 0:
            raise ValueError("Transport allowance cannot be negative")

        # Validate all percentages
        for pct, label in [
            (housing_allowance_pct, "HRA"),
            (tax_rate_pct, "Tax"),
            (da_pct, "DA"),
            (pf_pct, "PF"),
        ]:
            if not (Decimal("0") <= pct <= Decimal("1")):
                raise ValueError(f"{label} must be between 0 and 1")

        self.structure_id = structure_id
        self.name = name
        self.base_salary_min = base_salary_min
        self.base_salary_max = base_salary_max
        self.housing_allowance_pct = housing_allowance_pct
        self.transport_allowance = transport_allowance
        self.tax_rate_pct = tax_rate_pct
        self.da_pct = da_pct
        self.pf_pct = pf_pct

    def __repr__(self):
        return (
            f"SalaryStructure("
            f"ID={self.structure_id}, "
            f"Name='{self.name}', "
            f"Tax={self.tax_rate_pct * 100:.2f}%, "
            f"DA={self.da_pct * 100:.2f}%, "
            f"PF={self.pf_pct * 100:.2f}%)"
        )

    def to_dict(self):
        return {
            "structure_id": self.structure_id,
            "name": self.name,
            "base_salary_min": self.base_salary_min,
            "base_salary_max": self.base_salary_max,
            "housing_allowance_pct": self.housing_allowance_pct,
            "transport_allowance": self.transport_allowance,
            "tax_rate_pct": self.tax_rate_pct,
            "da_pct": self.da_pct,
            "pf_pct": self.pf_pct,
        }

    @staticmethod
    def from_db_record(record: dict):
        if not record:
            return None

        def safe_decimal(value):
            return Decimal(str(value)) if value is not None else Decimal("0.0")

        return SalaryStructure(
            structure_id=record["structure_id"],
            name=record["name"],
            base_salary_min=safe_decimal(record["base_salary_min"]),
            base_salary_max=safe_decimal(record["base_salary_max"]),
            housing_allowance_pct=safe_decimal(record.get("housing_allowance_pct")),
            transport_allowance=safe_decimal(record.get("transport_allowance")),
            tax_rate_pct=safe_decimal(record.get("tax_rate_pct")),
            da_pct=safe_decimal(record.get("da_pct")),
            pf_pct=safe_decimal(record.get("pf_pct")),
        )