import boto3
import sys
from botocore.exceptions import ClientError

def delete_object(bucket: str, key: str):
    s3 = boto3.client("s3")
    try:
        s3.delete_object(Bucket=bucket, Key=key)
        print(f"[OK] Deleted s3://{bucket}/{key}")
    except ClientError as e:
        print("[ERROR] delete_object failed:", e)
        raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 s3_delete_object.py <bucket> <key>")
        sys.exit(1)
    delete_object(sys.argv[1], sys.argv[2])
