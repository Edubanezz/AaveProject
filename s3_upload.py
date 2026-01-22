import boto3
import os
from datetime import datetime
from botocore.exceptions import ClientError

BUCKET_NAME = "mi-bucket-ejemplo-123456"
REGION = "eu-west-1"
LOCAL_BASE_PATH = "data"

s3 = boto3.client("s3", region_name=REGION)

def create_bucket(bucket_name, region):
    try:
        s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": region}
        )
        print(f"Bucket creado: {bucket_name}")
    except ClientError as e:
        if e.response["Error"]["Code"] == "BucketAlreadyOwnedByYou":
            print("El bucket ya existe")
        else:
            raise e

def upload_files(folder_type):
    now = datetime.now()
    year = now.year

    if folder_type == "daily":
        subfolder = f"day={now.strftime('%Y-%m-%d')}"
    else:
        subfolder = f"hour={now.strftime('%Y-%m-%d-%H')}"

    local_path = os.path.join(LOCAL_BASE_PATH, folder_type)

    for file in os.listdir(local_path):
        local_file = os.path.join(local_path, file)

        if os.path.isfile(local_file):
            s3_key = f"year={year}/{folder_type}/{subfolder}/{file}"

            s3.upload_file(local_file, BUCKET_NAME, s3_key)
            print(f"Subido: {s3_key}")

def main():
    create_bucket(BUCKET_NAME, REGION)
    upload_files("daily")
    upload_files("hourly")

if __name__ == "__main__":
    main()
