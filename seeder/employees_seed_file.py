import os
import json
import asyncio
import psycopg2
from config import connect_to_postgresql
from helper import get_utc_in_milliseconds_from_taipei_time


async def create_table():
    try:
        conn = await connect_to_postgresql()
        await conn.execute(
            """CREATE TABLE IF NOT EXISTS employees (
              id SERIAL PRIMARY KEY,
              employeeNumber INT NOT NULL,
              clockIn BIGINT CHECK (clockIn >= 0),
              clockOut BIGINT CHECK (clockOut >= 0));
          """)

        # print('Table created successfully.')

    except Exception:
        print("Create table error.")
    else:
        print('Table created successfully.')

    finally:
        await conn.close()


async def insert_data():
    try:
        conn = await connect_to_postgresql()
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
