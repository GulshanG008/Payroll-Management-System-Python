# database/connection.py

import mysql.connector
from mysql.connector import pooling
from mysql.connector import Error

class DBConnectionManager:
    """
    Manages the connection pool for the MySQL database.
    This class ensures connections are efficiently reused.
    """
    def __init__(self):
        # ⚠️ IMPORTANT: Load these credentials securely, ideally from a config file (like config/settings.py)
        # For this example, replace these placeholders with your actual MySQL details.
        self.host = "localhost"
        self.database = "payroll_db" 
        self.user = "root" 
        self.password = "your_mysql_password" # CHANGE THIS!
        
        # Connection Pool Configuration
        self.pool_name = "payroll_pool"
        self.pool_size = 5  # Max 5 simultaneous connections
        self._connection_pool = None
        
        self.initialize_pool()

    def initialize_pool(self):
        """Creates the MySQL connection pool."""
        try:
            self._connection_pool = pooling.MySQLConnectionPool(
                pool_name=self.pool_name,
                pool_size=self.pool_size,
                pool_reset_session=True, # Resets session state when connection is returned to pool
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password
            )
            print(f"Connection pool '{self.pool_name}' initialized with size {self.pool_size}.")
        except Error as e:
            print(f"Error initializing connection pool: {e}")
            self._connection_pool = None # Ensure pool is None on failure

    def get_connection(self):
        """
        Retrieves an available connection from the pool.
        The caller is responsible for returning the connection using release_connection().
        """
        if not self._connection_pool:
            print("Error: Connection pool is not initialized.")
            return None
            
        try:
            # Get connection from the pool
            conn = self._connection_pool.get_connection()
            return conn
        except Error as e:
            print(f"Error getting connection from pool: {e}")
            return None

    def release_connection(self, conn):
        """Returns the connection back to the pool."""
        if conn and conn.is_connected():
            # The pooled connection object has a built-in close() method 
            # that returns the connection to the pool, rather than truly closing it.
            conn.close()

# 💡 Singleton Instance:
# By instantiating the manager once at the module level, we ensure all parts 
# of the application use the same pool, avoiding initialization overhead.
connection_manager = DBConnectionManager()

def get_db_connection():
    """Public function to get a connection instance."""
    return connection_manager.get_connection()

def release_db_connection(conn):
    """Public function to release a connection instance."""
    connection_manager.release_connection(conn)