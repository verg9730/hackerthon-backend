import boto3
import botocore
from botocore.exceptions import ClientError
from botocore.client import Config

ACCESS_KEY_ID = "AKIAYE23XINAVFCGBIYA"
ACCESS_SECRET_KEY = "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"
BUCKET_NAME = "musiczzzzzzz"
"""
connect to S3
"""
client_s3 = boto3.client(
    's3',
    aws_access_key_id = ACCESS_KEY_ID,
    aws_secret_access_key = ACCESS_SECRET_KEY 
)

"""
upload file to S3
"""
def upload_file(location, file):
    try:
        client_s3.upload_file(
            location,
            BUCKET_NAME,
            file,
            ExtraArgs={'ContentType': 'image/jpeg'}
        )
    except ClientError as e :
        print(f'Credential error => {e}')
    except Exception as e :
        print(f"Another error => {e}")

def handle_upload_mp3(tmp_path, filename):
    s3_client = boto3.client('s3',
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=ACCESS_SECRET_KEY)
    response = s3_client.upload_file(
        tmp_path, BUCKET_NAME, filename)

def handle_upload_img(tmp_path, filename):
    data = open(tmp_path, 'rb')
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    s3.Bucket(BUCKET_NAME).put_object(
        Key=tmp_path, Body=data, ContentType='image/jpg')