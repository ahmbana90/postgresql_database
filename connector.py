import psycopg 
conn= psycopg.connect(
    host="localhost",
    dbname="myreadapp",
    user="postgres",
    password="0000",
    port=5432
)
print(conn)