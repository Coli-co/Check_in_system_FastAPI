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


async def find_employee_exist_or_not(employeeNumber):
    try:
        conn = await connect_to_postgresql()
        query = """
            SELECT * FROM employees WHERE employeenumber = $1
            """
        result = await conn.fetch(query, employeeNumber)
    except:
        print("Check employee in database error.")
    else:
        if len(result) > 0:
            print("Employee found in database.")
            return result
        print("No employee in database.")
        return result
    finally:
        await conn.close()


async def fillin_clockout_data(id, clockout):
    try:
        conn = await connect_to_postgresql()
        query = """
            UPDATE employees SET clockout = $2 WHERE id = $1
            """
        await conn.execute(query, id, clockout)
    except:
        print("Fill in clockout data error.")
        return False
    else:
        print("Fill in clockout data successfully.")
        return True
    finally:
        await conn.close()


async def fillin_clockin_data(id, clockin):
    try:
        conn = await connect_to_postgresql()
        query = """
            UPDATE employees SET clockin = $2 WHERE id = $1
            """
        await conn.execute(query, id, clockin)
    except:
        print("Fill in clockin data error.")
        return False
    else:
        print("Fill in clockin data successfully.")
        return True
    finally:
        await conn.close()


async def employee_with_clockin_earliest(date):
    try:
        conn = await connect_to_postgresql()
        query = """
            SELECT *  FROM employees
            WHERE clockin IS NOT NULL
                AND DATE_TRUNC('day', TO_TIMESTAMP(clockin / 1000.0)) = DATE_TRUNC('day', TO_TIMESTAMP($1 / 1000.0))
            ORDER BY clockin
            LIMIT 5;
        """
        result = await conn.fetch(query, date)
    except:
        print("Get clockin earliest employees data err.")
    else:
        print("Get clockin earliest employees data successfully.")
        return result
    finally:
        await conn.close()


async def employee_with_no_clockout(start, end):
    try:
        conn = await connect_to_postgresql()
        query = """
            SELECT *
            FROM employees
            WHERE clockOut IS NULL
            AND  TO_TIMESTAMP( clockIn / 1000.0) >= TO_TIMESTAMP($1 / 1000.0)
            AND  TO_TIMESTAMP( clockIn / 1000.0) <= TO_TIMESTAMP($2 / 1000.0) + INTERVAL '1 day - 1 second';         
        """
        result = await conn.fetch(query, start, end)
    except:
        print("Get no clockout employee data err.")
    else:
        print("Get no clockout employee data successfully.")
        return result
    finally:
        await conn.close()
