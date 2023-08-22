import psycopg2
from psycopg2 import Error


def create_connection():
    try:
        connection = psycopg2.connect(
            dbname="your_db_name",
            user="your_username",
            password="your_password",
            host="your_host",
            port="your_port"
        )
        print("Connected to the database successfully")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# FOR LOCAL DB
# DB_HOST=localhost
# DB_PORT=5432
# DB_USERNAME=husslup
# DB_PASSWORD=password
# DB_NAME=husslup-dev
# DB_SYNCRONIZE=true
# DB_LOGGING=true

# FOR DEV DB
# DB_HOST=husslup-db-dev.cycua6t8tsxn.us-west-1.rds.amazonaws.com
# DB_PORT=5432
# DB_USERNAME=postgres
# DB_PASSWORD=I8FdvNpSyKfOdRWGDKZH
# DB_NAME=husslup
# DB_SYNCRONIZE=false
# DB_LOGGING=true
