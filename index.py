from fastapi import FastAPI, HTTPException, status, Query, Path
from typing import Optional
from pydantic import BaseModel
from models import employees_for_specific_date_range, employees_for_specific_date, clockin_and_clockout, find_employee_exist_or_not, fillin_clockin_data, fillin_clockout_data, employee_with_clockin_earliest

from helper import process_employee_data, check_clockin_or_clockout, process_employee_exist_data

app = FastAPI()


class ClockInOutDataFilled(BaseModel):
    clockin: Optional[int] = None
    clockout: Optional[int] = None


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


@app.put('/employees/{employeenumber}')
async def fillin_clockin_or_clockout(data: ClockInOutDataFilled, employeenumber: int = Path(description="Clockin or clockout data of employeenumber you'd like to update.", gt=0)):
    clockin = data.clockin
    clockout = data.clockout
    employee_exist_data = await find_employee_exist_or_not(employeenumber)

    if len(employee_exist_data) == 0:
        raise HTTPException(
            status_code=200, detail="No related employeenumber.")

    have_clockin_or_clockout = await check_clockin_or_clockout(
        employee_exist_data, clockin, clockout)

    if not have_clockin_or_clockout:
        raise HTTPException(
            status_code=400, detail="You do not need to fill in clockin or clockout data.")
    process_data = await process_employee_exist_data(have_clockin_or_clockout)

    id = process_data[0]
    valid_time = process_data[1]

    if not valid_time:
        raise HTTPException(
            status_code=400, detail="Work time must be less than off-work time or off-work time must be greater than work time.")

    if not clockin and clockout is not None:
        update_clockout_result = await fillin_clockout_data(id, clockout)

        if update_clockout_result:
            raise HTTPException(
                status_code=201, detail="Clockout record updated successfully.")

    if not clockout and clockin is not None:
        update_clockin_result = await fillin_clockin_data(id, clockin)

        if update_clockin_result:
            raise HTTPException(
                status_code=201, detail="Clockin record updated successfully.")


@app.get('/employees/clockin-earliest')
async def employeesWithClockinEarliestForSpecificDate(date: int):
    if date <= 0:
        raise HTTPException(
            status_code=400, detail="Date must be greater than zero.")
    rows = await employee_with_clockin_earliest(date)
    result = await process_employee_data(rows)
    return result
