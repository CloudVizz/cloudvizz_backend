import psycopg2
from psycopg2 import sql, OperationalError

def create_connection(db_name, db_user, db_password, db_host, db_port):
    """Establishes a connection to the PostgreSQL database and returns the connection object."""
    connection = None
    try:
        connection = psycopg2.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection

def execute_query(connection, query):
    """Executes a single query"""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

# Define your database credentials
db_name = "cloudvizz"
db_user = "access"
db_password = "access"
db_host = "34.100.160.70"
db_port = "5432"  # default port for PostgreSQL is 5432

# Create a connection to the database
connection = create_connection(db_name, db_user, db_password, db_host, db_port)

# Test the connection by executing a simple query (optional)
if connection is not None:
    test_query = "SELECT version();"
    execute_query(connection, test_query)

# Don't forget to close the connection
if connection is not None:
    connection.close()
    print("Connection closed")
