from fastapi import HTTPException


def created_success(message):
    raise HTTPException(status_code=201, detail=message)


def bad_request_error(message):
    raise HTTPException(status_code=400, detail=message)


def not_found_error(message):
    raise HTTPException(status_code=404, detail=message)


def exception_error():
    raise HTTPException(status_code=500, detail="Internal Server Error.")
