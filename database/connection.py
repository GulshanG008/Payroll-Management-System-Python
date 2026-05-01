import pymysql
from config.db_config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME, DB_PORT


def get_db_connection():
    try:
        return pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT,
            cursorclass=pymysql.cursors.DictCursor
        )
    except Exception as e:
        raise Exception(f"Database connection failed: {e}")


def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(query, params or ())

        if fetch_one:
            return cursor.fetchone()

        if fetch_all:
            return cursor.fetchall()

        conn.commit()
        return cursor.lastrowid

    except Exception as e:
        conn.rollback()
        raise Exception(f"Query failed: {e}")

    finally:
        conn.close()