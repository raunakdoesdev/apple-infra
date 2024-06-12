from fastapi import FastAPI
import boto3

app = FastAPI()

@app.get("/")
def hello():
    return "Hello, World!"