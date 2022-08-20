import boto3
import botocore
from botocore.exceptions import ClientError
from botocore.client import Config

ACCESS_KEY_ID = "AKIAUGC2FVIMHZAKZPPL"
ACCESS_SECRET_KEY = "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"
BUCKET_NAME = "mymusic49848"
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

def handle_upload_mp3(f):
    s3_client = boto3.client('s3',
                            aws_access_key_id=ACCESS_KEY_ID,
                            aws_secret_access_key=ACCESS_SECRET_KEY)
    response = s3_client.upload_file(
        'C:/Users/hs922/Desktop/hackerthon-backend/'+f+'.mp3', BUCKET_NAME, f+'.mp3')

def handle_upload_img(f): # f = 파일명
    data = open('C:/Users/hs922/Desktop/hackerthon-backend/'+f+'.jpg', 'rb')
    # '로컬의 해당파일경로'+ 파일명 + 확장자
    s3 = boto3.resource(
        's3',
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=ACCESS_SECRET_KEY,
        config=Config(signature_version='s3v4')
    )
    s3.Bucket(BUCKET_NAME).put_object(
        Key=f, Body=data, ContentType='image/jpg')