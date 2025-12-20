# database/admin_dao.py

from typing import Optional

from database.connection import (
    get_db_connection,
    get_db_cursor,
    release_db_connection
)


class AdminDAO:
    """
    Data Access Object for Admin authentication.
    Handles admin login and admin management.
    """

    # --------------------------------------------------
    # CREATE ADMIN
    # --------------------------------------------------
    def create_admin(self, username: str, password_hash: str) -> int:
        query = """
            INSERT INTO admin (username, password_hash)
            VALUES (%s, %s)
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (username, password_hash))
            conn.commit()
            return cursor.lastrowid
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # AUTHENTICATE ADMIN (LOGIN)
    # --------------------------------------------------
    def get_by_username(self, username: str) -> Optional[dict]:
        query = """
            SELECT *
            FROM admin
            WHERE username = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (username,))
            return cursor.fetchone()
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # GET ADMIN BY ID
    # --------------------------------------------------
    def get_by_id(self, admin_id: int) -> Optional[dict]:
        query = """
            SELECT admin_id, username, created_at
            FROM admin
            WHERE admin_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (admin_id,))
            return cursor.fetchone()
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # UPDATE PASSWORD
    # --------------------------------------------------
    def update_password(self, admin_id: int, new_password_hash: str) -> bool:
        query = """
            UPDATE admin
            SET password_hash = %s
            WHERE admin_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (new_password_hash, admin_id))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)

    # --------------------------------------------------
    # DELETE ADMIN (OPTIONAL)
    # --------------------------------------------------
    def delete_admin(self, admin_id: int) -> bool:
        query = """
            DELETE FROM admin
            WHERE admin_id = %s
        """

        conn = get_db_connection()
        cursor = get_db_cursor(conn)

        try:
            cursor.execute(query, (admin_id,))
            conn.commit()
            return cursor.rowcount > 0
        finally:
            release_db_connection(conn)
