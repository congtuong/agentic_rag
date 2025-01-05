import sqlite3
import os
from sqlite3 import Connection

from .base import BaseDatabaseRepository

from utils.logger import get_logger

logger = get_logger()

class SQLiteDatabaseRepository(BaseDatabaseRepository):
    def __init__(self, db_path: str, init_db_path: str, reinit_db: bool = False):
        """Initialize the SQLite database repository."""
        self.db_path = db_path
        self.init_db_path = init_db_path
        logger.info(f"Database path: {self.db_path}")
        logger.info(f"Database health: {self.check_health()}")
        if reinit_db:
            logger.info(f"Initializing database with {init_db_path}")
            if os.path.exists(db_path):
                os.remove(db_path)
            with self.get_client() as conn:
                with open(init_db_path, 'r') as f:
                    sql = f.read()
                conn.executescript(sql)

    def _connect(self) -> Connection:
        """Connect to the SQLite database."""
        return sqlite3.connect(self.db_path)

    def get_client(self):
        """Get the SQLite database client."""
        return self._connect()

    def check_health(self) -> bool:
        """Check the health of the SQLite database."""
        try:
            with self.get_client() as conn:
                return True
        except Exception as e:
            logger.error(f"Error checking health of SQLite: {e}")
            return False
        
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Execute a query with optional fetch options."""
        try:
            with self.get_client() as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute(query, params if params else ())
                logger.info(f"Query executed: {query}")
                logger.info(f"Params: {params}")
                if fetch_one:
                    row = cursor.fetchone()
                    if row is None:
                        return False
                    return dict(row) if row else None
                if fetch_all:
                    return [dict(row) for row in cursor.fetchall()]
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None

    def create(self, table, **kwargs):
        """Create a new record in the specified table."""
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['?'] * len(kwargs))
        query = f"INSERT INTO {table} ({columns}, created_at, updated_at) VALUES ({placeholders}, datetime('now'), datetime('now'));"
        return self.execute_query(query, tuple(kwargs.values()))

    def read(self, table, record_id):
        """Retrieve a record by ID from the specified table."""
        query = f"SELECT * FROM {table} WHERE id = ?;"
        return self.execute_query(query, (record_id,), fetch_one=True)

    def update(self, table, record_id, **kwargs):
        """Update a record in the specified table."""
        fields = ', '.join([f"{key} = ?" for key in kwargs.keys()])
        query = f"UPDATE {table} SET {fields}, updated_at = datetime('now') WHERE id = ?;"
        return self.execute_query(query, (*kwargs.values(), record_id))

    def delete(self, table, record_id):
        """Delete a record from the specified table."""
        query = f"DELETE FROM {table} WHERE id = ?;"
        return self.execute_query(query, (record_id,))
        
    def read_by(self, table, column, value):
        """Retrieve a record by a specified column value."""
        query = f"SELECT * FROM {table} WHERE {column} = ?;"
        return self.execute_query(query, (value,), fetch_one=True)