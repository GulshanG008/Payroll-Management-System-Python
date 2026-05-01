import pymysql


def get_db_connection():
    try:
        conn = pymysql.connect(
            host="localhost",
            user="root",
            password="",  # XAMPP default
            database="payroll_management",
            port=3306,
            cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        print("DB Connection Error:", e)
        return None


def get_db_cursor(conn):
    return conn.cursor()


def release_db_connection(conn):
    if conn:
        conn.close()