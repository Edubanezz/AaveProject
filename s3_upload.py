import os
import boto3
from botocore.exceptions import ClientError

BUCKET_NAME = "mi-bucket-datos-aave-2026"  # CAMBIA EL NOMBRE
BASE_PATH = "Data"
YEARS = ["2022", "2023", "2024", "2025"]
REGION = "eu-south-2"

def create_bucket():
    s3_client = boto3.client("s3", region_name=REGION)

    try:
        s3_client.create_bucket(
            Bucket=BUCKET_NAME,
            CreateBucketConfiguration={"LocationConstraint": REGION}
        )
        print(f"Bucket creado: {BUCKET_NAME}")
    except ClientError as e:
        error = e.response["Error"]["Code"]
        if error == "BucketAlreadyOwnedByYou":
            print("Bucket ya existe")
        else:
            raise e

def upload_file(bucket, local_file, s3_key):
    if os.path.exists(local_file):
        bucket.upload_file(local_file, s3_key)
        print(f"Subido: {s3_key}")

def main():
    create_bucket()

    s3 = boto3.resource("s3", region_name=REGION)
    bucket = s3.Bucket(BUCKET_NAME)

    for year in YEARS:
        year_path = os.path.join(BASE_PATH, f"YEAR={year}")

        daily = os.path.join(year_path, "AAVEUSD_daily.csv")
        monthly = os.path.join(year_path, "AAVEUSD_monthly.csv")

        upload_file(bucket, daily, f"year={year}/daily/AAVEUSD_daily.csv")
        upload_file(bucket, monthly, f"year={year}/monthly/AAVEUSD_monthly.csv")

if __name__ == "__main__":
    main()
