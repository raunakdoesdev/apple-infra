FROM python:3.11

WORKDIR /code

RUN pip install boto3 fastapi uvicorn

COPY app.py app.py

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]