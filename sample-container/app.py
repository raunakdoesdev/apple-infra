from fastapi import FastAPI
from typing import Literal
import boto3
import os

ROLE_SESSION_NAMES = {
    "textract": os.environ.get("AWS_TEXTRACT_ROLE_SESSION_NAME", "reducto_textract"),
    "s3": os.environ.get("AWS_S3_ROLE_SESSION_NAME", "reducto_s3")
}

def get_client(client_type: Literal["textract", "s3"], region: str = None):
    sts_connection = boto3.client("sts")
    with open(os.environ["AWS_WEB_IDENTITY_TOKEN_FILE"], "r") as f:
        web_identity_token = f.read().strip()

    assume_role_object = sts_connection.assume_role_with_web_identity(
        RoleArn=os.environ["AWS_ROLE_ARN"],
        RoleSessionName=ROLE_SESSION_NAMES.get(client_type, f"reducto_{client_type}"),
        WebIdentityToken=web_identity_token
    )

    if region is None:
        region_name = os.environ.get('AWS_REGION', 'us-west-2'),

    return boto3.client(
        client_type,
        aws_access_key_id=assume_role_object['Credentials']['AccessKeyId'],
        aws_secret_access_key=assume_role_object['Credentials']['SecretAccessKey'],
        aws_session_token=assume_role_object['Credentials']['SessionToken'],
        region_name=region_name
    )


app = FastAPI()


@app.get("/")
def hello():
    return "Hello, World!"



@app.get("/textract")
def textract():
    with open("sample.png", "rb") as f:
        bytes = f.read()
    client = get_client("textract")
    response = client.detect_document_text(
        Document={
            "Bytes": bytes
        }
    )

    return "\n".join([block["Text"] for block in response["Blocks"] if block["BlockType"] == "LINE"])


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
