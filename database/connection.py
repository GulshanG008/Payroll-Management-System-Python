# database/connection.py

import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error

class DBConnectionManager:
    def __init__(self):
        self.database = "payroll_db" 
        self.user = "root" 
        self.password = "your_mysql_password" # CHANGE THIS!
        
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
            print(f"Connection pool '{self.pool_name}' initialized with size {self.pool_size}.")
        except Error as e:
            print(f"Error initializing connection pool: {e}")
            self._connection_pool = None

    def get_connection(self):
        if not self._connection_pool:
            print("Error: Connection pool is not initialized.")
            return None
            
        try:
            conn = self._connection_pool.get_connection()
            return conn
        except Error as e:
            print(f"Error getting connection from pool: {e}")
            return None

    def release_connection(self, conn):
        if conn and conn.is_connected():
            conn.close()

connection_manager = DBConnectionManager()

def get_db_connection():
    return connection_manager.get_connection()

def release_db_connection(conn):
    connection_manager.release_connection(conn)