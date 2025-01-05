import psycopg2

from .base import BaseDatabaseRepository

class PostgresDatabaseRepository(BaseDatabaseRepository):
    def __init__(
        self,
        host: str,
        port: int,
        database: str,
        user: str,
        password: str,
    ):
        """
        Initialize the Postgres database repository.
        """
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        
        super().__init__()
    
    def _connect(self):
        """
        Connect to the Postgres database.
        """
        pass
    
    def get_client(self):
        """
        Get the Postgres database client.
        """
        try:
            conn = psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password,
            )
            return conn
        except Exception as e:
            logger.error(f"Error connecting to Postgres: {e}")
            return None

    def check_health(self) -> bool:
        """
        Check the health of the Postgres database.
        """
        try:
            conn = self.get_client()
            if conn is None:
                return False
            conn.close()
            return True
        except Exception as e:
            logger.error(f"Error checking health of Postgres: {e}")
            return False
        
    def execute_query(self, query, params=None, fetch_one=False, fetch_all=False):
        """Execute a query with optional fetch options."""
        try:
            with self._connect() as conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    cursor.execute(query, params)
                    if fetch_one:
                        return cursor.fetchone()
                    if fetch_all:
                        return cursor.fetchall()
                    conn.commit()
        except Exception as e:
            logger.error(f"Error executing query: {e}")
            return None

    def create(self, table: str, **kwargs):
        """Create a new record in the specified table."""
        columns = ', '.join(kwargs.keys())
        placeholders = ', '.join(['%s'] * len(kwargs))
        query = f"INSERT INTO {table} ({columns}, created_at, updated_at) VALUES ({placeholders}, NOW(), NOW()) RETURNING id;"
        return self.execute_query(query, tuple(kwargs.values()), fetch_one=True)['id']

    def read(self, table: str, record_id: str):
        """Retrieve a record by ID from the specified table."""
        query = f"SELECT * FROM {table} WHERE id = %s;"
        return self.execute_query(query, (record_id,), fetch_one=True)

    def update(self, table: str, record_id: str, **kwargs):
        """Update a record in the specified table."""
        fields = ', '.join([f"{key} = %s" for key in kwargs.keys()])
        query = f"UPDATE {table} SET {fields}, updated_at = NOW() WHERE id = %s;"
        self.execute_query(query, (*kwargs.values(), record_id))

    def delete(self, table: str, record_id: str):
        """Delete a record from the specified table."""
        query = f"DELETE FROM {table} WHERE id = %s;"
        self.execute_query(query, (record_id,))
        
        
    