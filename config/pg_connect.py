import os
import asyncio
import asyncpg
from dotenv import load_dotenv


load_dotenv()


async def connect_to_postgresql():
    try:
        connection = await asyncpg.connect(
            host=os.getenv("PGHOST"),
            database=os.getenv("PGDB"),
            user=os.getenv("PGUSER"),
            password=os.getenv("PGPASSWORD")
        )

    except Exception as err:
        print("Connecting to PostgreSQL error:", err)
        return None, None
    else:
        print('DB connection established.')
        return connection
