from fastapi import FastAPI, HTTPException, status, Query
from models import employees_for_specific_date_range

from helper import process_employee_data

app = FastAPI()


@app.get('/')
def homepage():
    raise HTTPException(
        status_code=200, detail='Welcome to employees clockIn or clockOut API server.')


@app.get('/employees')
async def all_employees_for_specific_date(start: str, end: str):
    if int(start) <= 0 or int(end) <= 0:
        raise HTTPException(
            status_code=400, detail="Start or end must be grater than zero.")

    if int(start) > int(end):
        raise HTTPException(
            status_code=400, detail="Start value must be less than end value.")

    rows = await employees_for_specific_date_range(start, end)
    result = await process_employee_data(rows)
    return result
