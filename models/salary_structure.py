# models/salary_structure.py

from decimal import Decimal

class SalaryStructure:
    """
    Data model for defining a salary structure, including base components 
    like allowances and fixed deductions.
    """
    def __init__(self, 
                 structure_id: int, 
                 name: str, 
                 base_salary_min: Decimal, 
                 base_salary_max: Decimal,
                 housing_allowance_pct: Decimal = Decimal('0.0'),
                 transport_allowance: Decimal = Decimal('0.0'),
                 tax_rate_pct: Decimal = Decimal('0.0')):
        
        self.structure_id = structure_id
        self.name = name
        self.base_salary_min = base_salary_min
        self.base_salary_max = base_salary_max
        # Allowances (stored as a percentage of base salary or fixed amount)
        self.housing_allowance_pct = housing_allowance_pct
        self.transport_allowance = transport_allowance # Fixed monthly amount
        # Deductions
        self.tax_rate_pct = tax_rate_pct

    def __repr__(self):
        """Provides a helpful string representation for debugging."""
        return f"SalaryStructure(ID={self.structure_id}, Name='{self.name}', Tax={self.tax_rate_pct * 100:.2f}%)"

    def to_dict(self):
        """Converts the SalaryStructure object into a dictionary."""
        return {
            "structure_id": self.structure_id,
            "name": self.name,
            "base_salary_min": self.base_salary_min,
            "base_salary_max": self.base_salary_max,
            "housing_allowance_pct": self.housing_allowance_pct,
            "transport_allowance": self.transport_allowance,
            "tax_rate_pct": self.tax_rate_pct
        }

    @staticmethod
    def from_db_record(record: dict):
        """
        Static method to create a SalaryStructure object from a database dictionary record.
        Ensures all numerical values are converted to Decimal for accuracy.
        """
        def safe_decimal(value):
            return Decimal(str(value)) if value is not None else Decimal('0.0')

        return SalaryStructure(
            structure_id=record.get('structure_id'),
            name=record.get('name'),
            base_salary_min=safe_decimal(record.get('base_salary_min')),
            base_salary_max=safe_decimal(record.get('base_salary_max')),
            housing_allowance_pct=safe_decimal(record.get('housing_allowance_pct')),
            transport_allowance=safe_decimal(record.get('transport_allowance')),
            tax_rate_pct=safe_decimal(record.get('tax_rate_pct'))
        )