FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt /app/

RUN cd /app/
RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt

COPY . /app/

ENV PYTHONPATH=/app


CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]

