# database/salary_dao.py

from decimal import Decimal
from typing import List, Optional

from database.connection import (
    get_db_connection,
    get_db_cursor,
    release_db_connection
)
from models.salary_structure import SalaryStructure


class SalaryDAO:
    """
    Data Access Object for Salary Structure table.
    Handles all database operations related to salary structures.
    """

    # --------------------------------------------------
    # CREATE
    # --------------------------------------------------
    def create_salary_structure(self, structure: SalaryStructure) -> int:
        query = """
            INSERT INTO salary_structure (
                name,
                base_salary_min,
                base_salary_max,
                housing_allowance_pct,
                transport_allowance,
                tax_rate_pct
            )
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(
                query,
                (
                    structure.name,
                    structure.base_salary_min,
                    structure.base_salary_max,
                    structure.housing_allowance_pct,
                    structure.transport_allowance,
                    structure.tax_rate_pct,
                )
            )
            conn.commit()
            return cursor.lastrowid

        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # READ BY ID
    # --------------------------------------------------
    def get_by_id(self, structure_id: int) -> Optional[SalaryStructure]:
        query = """
            SELECT *
            FROM salary_structure
            WHERE structure_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (structure_id,))
            record = cursor.fetchone()
            return (
                SalaryStructure.from_db_record(record)
                if record else None
            )
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # READ ALL
    # --------------------------------------------------
    def get_all(self) -> List[SalaryStructure]:
        query = """
            SELECT *
            FROM salary_structure
            ORDER BY base_salary_min ASC
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query)
            records = cursor.fetchall()
            return [
                SalaryStructure.from_db_record(r)
                for r in records
            ]
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # FIND STRUCTURE FOR BASIC SALARY
    # --------------------------------------------------
    def get_structure_for_salary(
        self,
        basic_salary: Decimal
    ) -> Optional[SalaryStructure]:
        """
        Finds salary structure where:
        base_salary_min <= basic_salary <= base_salary_max
        """

        query = """
            SELECT *
            FROM salary_structure
            WHERE %s BETWEEN base_salary_min AND base_salary_max
            LIMIT 1
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (basic_salary,))
            record = cursor.fetchone()
            return (
                SalaryStructure.from_db_record(record)
                if record else None
            )
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------
    def update_salary_structure(self, structure: SalaryStructure) -> bool:
        query = """
            UPDATE salary_structure
            SET
                name = %s,
                base_salary_min = %s,
                base_salary_max = %s,
                housing_allowance_pct = %s,
                transport_allowance = %s,
                tax_rate_pct = %s
            WHERE structure_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(
                query,
                (
                    structure.name,
                    structure.base_salary_min,
                    structure.base_salary_max,
                    structure.housing_allowance_pct,
                    structure.transport_allowance,
                    structure.tax_rate_pct,
                    structure.structure_id,
                )
            )
            conn.commit()
            return cursor.rowcount > 0

        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # DELETE
    # --------------------------------------------------
    def delete_salary_structure(self, structure_id: int) -> bool:
        query = """
            DELETE FROM salary_structure
            WHERE structure_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (structure_id,))
            conn.commit()
            return cursor.rowcount > 0

        finally:
            release_db_connection(conn)
