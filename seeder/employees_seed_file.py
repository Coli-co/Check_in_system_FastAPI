import os
import json
import asyncio
import asyncpg
from config import connect_to_postgresql
from helper import get_utc_in_milliseconds_from_taipei_time
from dotenv import load_dotenv
import traceback
load_dotenv()


async def db_connect():
    try:
        connection = await asyncpg.connect(
            host='localhost',
            database=os.getenv("PGDB"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD"),
            port=5431
        )

    except Exception as err:
        traceback.print_exc()
        print("Connecting to PostgreSQL error:", err)
        return None
    else:
        print('DB connection established.')
    return connection


async def create_table():
    try:
        conn = await db_connect()
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS employees (
            id SERIAL PRIMARY KEY,
            employeeNumber INT NOT NULL,
            clockIn BIGINT CHECK (clockIn >= 0),
            clockOut BIGINT CHECK (clockOut >= 0));
          """)
    except Exception:
        print("Create table error.")
    else:
        print('Table created successfully.')
        return conn
    finally:
        await conn.close()


async def insert_data():
    try:
        conn = await db_connect()
        curr_dir = os.path.dirname(os.path.abspath(__file__))

        json_file_path = os.path.join(curr_dir, '..', 'public', 'member.json')

        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

            for employee in data:
                employeeNumber = employee['employeeNumber']

                clockIn = None if employee['clockIn'] is None else await get_utc_in_milliseconds_from_taipei_time(employee['clockIn']) or null

                clockOut = None if employee['clockOut'] is None else await get_utc_in_milliseconds_from_taipei_time(employee['clockOut']) or null

                insert_query = """
                  INSERT INTO employees (employeeNumber, clockIn, clockOut) VALUES ($1, $2, $3)
                """

                await conn.execute(insert_query, employeeNumber, clockIn, clockOut)
    except Exception as err:
        print('Insert data error.', err)
    else:
        print('Data inserted successfully.')
    finally:
        await conn.close()


asyncio.run(create_table())
asyncio.run(insert_data())
