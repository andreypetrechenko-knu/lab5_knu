import boto3
import sys
from botocore.exceptions import ClientError

REGION = "eu-north-1"

def create_bucket(bucket_name: str):
    s3 = boto3.client("s3", region_name=REGION)

    try:
        response = s3.create_bucket(
            Bucket=bucket_name,
            CreateBucketConfiguration={"LocationConstraint": REGION}
        )

        print(f"[OK] Bucket created: {bucket_name}")
        print(response)

    except ClientError as e:
        code = e.response["Error"]["Code"]

        if code in ("BucketAlreadyExists", "BucketAlreadyOwnedByYou"):
            print(f"[WARN] Bucket name conflict: {code}")
        else:
            print("[ERROR] create_bucket failed:", e)
            raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 s3_create.py <bucket-name>")
        sys.exit(1)

    create_bucket(sys.argv[1])
