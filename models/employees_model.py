from config import connect_to_postgresql


async def employees_for_specific_date_range(start, end):
    try:
        conn = await connect_to_postgresql()
        query = """
        SELECT * FROM employees
        WHERE (DATE_TRUNC('day', COALESCE(TO_TIMESTAMP(NULLIF(clockin, 0) / 1000.0), TO_TIMESTAMP(NULLIF(clockout, 0) / 1000.0))) >= DATE_TRUNC('day', TO_TIMESTAMP($1 / 1000.0)))
        AND (DATE_TRUNC('day', COALESCE(TO_TIMESTAMP(NULLIF(clockin, 0) / 1000.0), TO_TIMESTAMP(NULLIF(clockout, 0) / 1000.0))) <= DATE_TRUNC('day', TO_TIMESTAMP($2 / 1000.0) + INTERVAL '1 day - 1 second'));
        """
        result = await conn.fetch(query, start, end)
    except Exception:
        print("Get employeesForSpecificDateRange data err.")
    else:
        print("Get employeesForSpecificDateRange data successfully.")

        return result
    finally:
        await conn.close()


async def employees_for_specific_date(date):
    try:
        conn = await connect_to_postgresql()
        query = """
        SELECT *  FROM employees
        WHERE DATE_TRUNC('day', COALESCE(TO_TIMESTAMP(NULLIF(clockin, 0) / 1000.0), TO_TIMESTAMP(NULLIF(clockout, 0) / 1000.0))) = DATE_TRUNC('day', TO_TIMESTAMP($1 / 1000.0));
        """
        result = await conn.fetch(query, date)
    except Exception:
        print("Get employeesForSpecificDate data err.")
        return False
    else:
        print("Get employeesForSpecificDate data successfully.")
        return result
    finally:
        await conn.close()


async def clockin_and_clockout(employeeNumber, clockIn, clockOut):
    try:
        conn = await connect_to_postgresql()
        query = """
            INSERT INTO employees (employeenumber, clockin, clockout) VALUES ($1, $2, $3)
            """
        await conn.execute(query, employeeNumber, clockIn, clockOut)
    except:
        print("Clockin and clockout data inserted error.")
        return False
    else:
        print("New employee data inserted successfully.")
        return True
    finally:
        await conn.close()
