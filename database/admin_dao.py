# database/admin_dao.py

from typing import Optional
from database.connection import execute_query


class AdminDAO:

    def create_admin(self, username: str, password_hash: str) -> int:
        query = """
            INSERT INTO admin (username, password_hash)
            VALUES (%s, %s)
        """
        return execute_query(query, (username, password_hash))

    def get_by_username(self, username: str) -> Optional[dict]:
        query = """
            SELECT *
            FROM admin
            WHERE username = %s
        """
        return execute_query(query, (username,), fetch_one=True)

    def get_by_id(self, admin_id: int) -> Optional[dict]:
        query = """
            SELECT admin_id, username, created_at
            FROM admin
            WHERE admin_id = %s
        """
        return execute_query(query, (admin_id,), fetch_one=True)

    def update_password(self, admin_id: int, new_password_hash: str) -> bool:
        query = """
            UPDATE admin
            SET password_hash = %s
            WHERE admin_id = %s
        """
        result = execute_query(query, (new_password_hash, admin_id))
        return result is not None

    def delete_admin(self, admin_id: int) -> bool:
        query = """
            DELETE FROM admin
            WHERE admin_id = %s
        """
        result = execute_query(query, (admin_id,))
        return result is not None