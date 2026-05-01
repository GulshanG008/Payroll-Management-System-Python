from decimal import Decimal
from typing import List, Optional

from database.connection import execute_query
from models.salary_structure import SalaryStructure


class SalaryDAO:

    def create_salary_structure(self, structure: SalaryStructure) -> int:

        if structure.base_salary_min > structure.base_salary_max:
            raise ValueError("Min salary cannot exceed max salary")

        query = """
            INSERT INTO salary_structure (
                name, base_salary_min, base_salary_max,
                housing_allowance_pct, transport_allowance,
                tax_rate_pct, da_pct, pf_pct
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """

        return execute_query(
            query,
            (
                structure.name,
                structure.base_salary_min,
                structure.base_salary_max,
                structure.housing_allowance_pct,
                structure.transport_allowance,
                structure.tax_rate_pct,
                structure.da_pct,
                structure.pf_pct,
            ),
        )

    def get_by_id(self, structure_id: int) -> Optional[SalaryStructure]:
        query = "SELECT * FROM salary_structure WHERE structure_id = %s"

        record = execute_query(query, (structure_id,), fetch_one=True)
        return SalaryStructure.from_db_record(record) if record else None

    def get_all(self) -> List[SalaryStructure]:
        query = """
            SELECT *
            FROM salary_structure
            ORDER BY base_salary_min ASC
        """

        records = execute_query(query, fetch_all=True)
        return [SalaryStructure.from_db_record(r) for r in records]

    def get_structure_for_salary(self, basic_salary: Decimal) -> Optional[SalaryStructure]:
        query = """
            SELECT *
            FROM salary_structure
            WHERE %s BETWEEN base_salary_min AND base_salary_max
            LIMIT 1
        """

        record = execute_query(query, (basic_salary,), fetch_one=True)
        return SalaryStructure.from_db_record(record) if record else None

    def update_salary_structure(self, structure: SalaryStructure) -> bool:

        if structure.base_salary_min > structure.base_salary_max:
            raise ValueError("Invalid salary range")

        query = """
            UPDATE salary_structure
            SET name=%s,
                base_salary_min=%s,
                base_salary_max=%s,
                housing_allowance_pct=%s,
                transport_allowance=%s,
                tax_rate_pct=%s,
                da_pct=%s,
                pf_pct=%s
            WHERE structure_id = %s
        """

        result = execute_query(
            query,
            (
                structure.name,
                structure.base_salary_min,
                structure.base_salary_max,
                structure.housing_allowance_pct,
                structure.transport_allowance,
                structure.tax_rate_pct,
                structure.da_pct,
                structure.pf_pct,
                structure.structure_id,
            ),
        )

        return result is not None

    def delete_salary_structure(self, structure_id: int) -> bool:
        query = "DELETE FROM salary_structure WHERE structure_id = %s"
        result = execute_query(query, (structure_id,))
        return result is not None