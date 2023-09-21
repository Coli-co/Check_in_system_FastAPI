from fastapi import FastAPI, HTTPException, status, Query
from typing import Optional
from models import employees_for_specific_date_range, employees_for_specific_date, clockin_and_clockout

from helper import process_employee_data

app = FastAPI()


@app.get('/')
def homepage():
    raise HTTPException(
        status_code=200, detail='Welcome to employees clockIn or clockOut API server.')


@app.get('/employees/date-range')
async def all_employees_for_specific_date_range(start: int, end: int):
    if start <= 0 or end <= 0:
        raise HTTPException(
            status_code=400, detail="Start or end must be grater than zero.")

    if start > end:
        raise HTTPException(
            status_code=400, detail="Start value must be less than end value.")

    rows = await employees_for_specific_date_range(start, end)
    result = await process_employee_data(rows)
    return result


@app.get('/employees')
async def all_employees_for_specific_date(date: int):
    if date <= 0:
        raise HTTPException(
            status_code=400, detail="Date value must be greater than zero.")
    rows = await employees_for_specific_date(date)
    result = await process_employee_data(rows)
    return result


@app.post('/employees')
async def clock_feature(employeeNumber: int, clockin: Optional[int] = None, clockout: Optional[int] = None):

    if not clockin and not clockout:
        raise HTTPException(
            status_code=400, detail="Clockin or clockout required.")

    if not clockout and clockin <= 0:
        raise HTTPException(
            status_code=400, detail="Clockin must be greater than zero.")

    if not clockin and clockout <= 0:
        raise HTTPException(
            status_code=400, detail="Clockout must be greater than zero.")

    if clockin is not None and clockout is not None and clockin > clockout:
        raise HTTPException(
            status_code=400, detail="Clockin value must be less than clockout.")

    rowCount = await clockin_and_clockout(employeeNumber, clockin, clockout)

    if rowCount:
        if clockout is None and clockin > 0:
            raise HTTPException(
                status_code=201, detail="Clockin record created successfully.")

        elif clockin is None and clockout > 0:
            raise HTTPException(
                status_code=201, detail="Clockout record created successfully.")

        raise HTTPException(
            status_code=201, detail="Employee record created successfully.")
