import os
import psycopg2
from dotenv import load_dotenv


load_dotenv()


def connect_to_postgresql():
    try:
        connection = psycopg2.connect(
            host=os.getenv("PGHOST"),
            database=os.getenv("PGDB"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD")
        )
        connection.autocommit = True

        cursor = connection.cursor()
        print('DB connection established.')
        return connection, cursor

    except psycopg2.Error as error:
        print("Connecting to PostgreSQL error:", error)
        return None, None
