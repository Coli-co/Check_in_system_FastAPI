from fastapi import FastAPI, HTTPException, status


app = FastAPI()


@app.get('/')
def homepage():
    raise HTTPException(
        status_code=200, detail='Welcome to employees clockIn or clockOut API server.')
