FROM python:3.11

WORKDIR /code

RUN pip install boto3 fastapi

COPY app.py app.py
COPY sample.png sample.png

CMD ["fastapi", "run", "app.py", "--port", "80"]