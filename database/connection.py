# database/connection.py
import mysql.connector
from mysql.connector import pooling, Error


class DBConnectionManager:
    """
    Manages MySQL connection pooling for the Payroll Management System.
    """

    def __init__(self):
        # ---- DATABASE CONFIG ----
        self.host = "localhost"
        self.database = "payroll_db"
        self.user = "root"
        self.password = "your_mysql_password"  # CHANGE THIS

        # ---- POOL CONFIG ----
        self.pool_name = "payroll_pool"
        self.pool_size = 5

        self._connection_pool = None
        self.initialize_pool()

    def initialize_pool(self):
        try:
            self._connection_pool = pooling.MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                pool_reset_session=True,
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print(
                f"✅ Connection pool '{self.pool_name}' "
                f"initialized with size {self.pool_size}"
            )
        except Error as e:
            raise Exception(f"❌ Failed to initialize DB connection pool: {e}")

    def get_connection(self):
        """
        Get a connection from the pool.
        """
        try:
            return self._connection_pool.get_connection()
        except Error as e:
            raise Exception(f"❌ Unable to get DB connection: {e}")

    def get_cursor(self, conn, dictionary=True):
        """
        Get a cursor from a connection.
        """
        return conn.cursor(dictionary=dictionary)

    def release_connection(self, conn):
        """
        Release connection back to pool.
        """
        if conn and conn.is_connected():
            conn.close()


# ---- SINGLETON INSTANCE ----
connection_manager = DBConnectionManager()


def get_db_connection():
    return connection_manager.get_connection()


def get_db_cursor(conn, dictionary=True):
    return connection_manager.get_cursor(conn, dictionary)


def release_db_connection(conn):
    connection_manager.release_connection(conn)
