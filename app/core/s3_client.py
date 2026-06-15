import os
import boto3
from botocore.config import Config
from dotenv import load_dotenv

load_dotenv()

S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "optistream-invoices")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID", "minioadmin")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY", "minioadmin")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")

# Crucial variable: If set, we point to boto3 to our local MinIO server instead of actual AWS
S3_ENDPIONT_URL = os.getenv("S3_ENDPIONT_URL", "http://localhost:9000")

def get_s3_client():
    """
    Construct a thread-safe Boto3 S3 client dynamically.
    Configures signatures version 's3v4' explicitly for secure presigned URL generation.
    """
    s3_config = Config(signature_version='s3v4')

    #If  S3_ENDPOINT_URL is present, we are emulating AWS locally via MinIO
    if S3_ENDPIONT_URL:
        return boto3.client(
            's3',
            endpoint_url=S3_ENDPIONT_URL,
            aws_access_key_id = AWS_ACCESS_KEY_ID,
            aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
            region_name = AWS_REGION,
            config = s3_config
        )
    
    # standard production AWS cofiguration
    return boto3.client(
        's3',
        aws_access_key_id = AWS_ACCESS_KEY_ID,
        aws_secret_access_key = AWS_SECRET_ACCESS_KEY,
        region_name = AWS_REGION,
        config = s3_config
    )

