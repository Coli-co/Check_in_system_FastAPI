from fastapi import FastAPI, HTTPException, status, Path
from controller import all_employees_for_specific_date, all_employees_for_specific_date_range, clock_feature, ClockFeature, fillin_clockin_or_clockout, ClockInOutDataFilled, employees_with_clockin_earliest_for_specific_date, employees_with_no_clockout_for_specific_date_range


app = FastAPI()


@app.get('/')
def homepage():
    raise HTTPException(
        status_code=200, detail='Welcome to employees clockIn or clockOut API server.')


@app.get('/employees')
async def get_all_employees_for_specific_date(date: int):
    result = await all_employees_for_specific_date(date)
    return result


@app.get('/employees/date-range')
async def get_employees_for_specific_date_range(start: int, end: int):
    result = await all_employees_for_specific_date_range(start, end)
    return result


@app.post('/employees')
async def employees_clock_feature(employeenumber: int, data: ClockFeature):
    result = await clock_feature(employeenumber, data)
    return result


@app.put('/employees/{employeenumber}')
async def fillin_clockin_clockout_feature(data: ClockInOutDataFilled, employeenumber: int = Path(description="Clockin or clockout data of employeenumber you'd like to update.", gt=0)):
    result = await fillin_clockin_or_clockout(data, employeenumber)
    return result


@app.get('/employees/clockin-earliest')
async def get_employees_with_clockin_earliest_for_specific_date(date: int):
    result = await employees_with_clockin_earliest_for_specific_date(date)
    return result


@app.get('/employees/no-clockout')
async def get_employees_with_no_clockout_for_specific_date_range(start: int, end: int):
    result = await employees_with_no_clockout_for_specific_date_range(start, end)
    return result
