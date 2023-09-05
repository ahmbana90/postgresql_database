import psycopg as pg
from datetime import date
import environ
from src.util import ROOT_DIR
from src.schema import CreateDataType, FetchByIdDataType
from typing import Optional, Union

# Create a connection

env= environ.Env()

# Set .env from root dir to read

environ.Env.read_env(str(ROOT_DIR / '.env'))

# Singleton class
class Database:
    _instance= None
    
    def __new__(cls):
        if Database._instance is None:
            Database._instance= super().__new__(cls)
            Database._instance.__init__()
            
        return Database._instance._conn
    
    def __init__(self) -> None:
        self._conn= pg.connect(
            host=env.str("db_host"),
            dbname=env.str("db_name"),
            user=env.str("db_user"),
            password=env.str("db_password"),
            port=env.int("db_port")
        )

def update_data(book_id: int, column: str, data: Union[str, date, int]) -> Optional[int]:
    conn= Database()
    query= """
        UPDATE read.book
        SET """+ column +"""=%s
        WHERE id=%s RETURNING id;
    """
    with conn.cursor() as cursor:
        cursor.execute(query, [data, book_id])
        updated_book_id= cursor.fetchone()[0]
        conn.commit()
        return updated_book_id

def fetch_by_id(book_id: int) -> Optional[FetchByIdDataType]:
    conn= Database()
    
    query= """
        SELECT
            title,
            des,
            status,
            pct_read,
            start_read_date,
            end_read_date
        FROM read.book
        WHERE id=%s;
    """    
    with conn.cursor() as cursor:
        cursor.execute(query,(book_id, ))
        book= cursor.fetchone()
        return book
        
def insert_data(data: CreateDataType) -> Optional[int]:
    # get the connection
    conn= Database()
    # define the query
    query= """
        INSERT INTO read.book(
            username,
            title,
            des,
            status,
            pct_read,
            start_read_date,
            end_read_date
        ) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;
    """
    # create a cursor session
    with conn.cursor() as cursor:
    # use the cursor session to execute the query
        cursor.execute(query, tuple(data.values()))
        inserted_id= cursor.fetchone()[0]
        conn.commit()
        return inserted_id