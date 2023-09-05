import unittest
from src.database import Database

# we want to test for singleton
# we want to test database connectivity

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.conn = Database()
        
    # singleton
    def test_singleton(self):
        conn1= Database()
        conn2= Database()
        
        self.assertEqual(conn1, conn2)
    
    def test_postgres_version(self):
        pg_version= "PostgreSQL 14.8"
        with self.conn.cursor() as cursor:
            cursor.execute("SELECT version();")  # execute sql statement
            db_version= cursor.fetchone()[0]  # get on row
            self.assertTrue(db_version.startswith(pg_version))
            
            
    def tearDown(self) -> None:
        self.conn.close()