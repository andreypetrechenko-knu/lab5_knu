import boto3
import sys
import os
from botocore.exceptions import ClientError

def upload_file(bucket: str, file_path: str, key: str):
    if not os.path.exists(file_path):
        print(f"[ERROR] Local file not found: {file_path}")
        return

    s3 = boto3.client("s3")
    try:
        s3.upload_file(Filename=file_path, Bucket=bucket, Key=key)
        print(f"[OK] Uploaded {file_path} -> s3://{bucket}/{key}")
    except ClientError as e:
        print("[ERROR] upload_file failed:", e)
        raise

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 s3_upload.py <bucket> <file_path> <key>")
        sys.exit(1)
    upload_file(sys.argv[1], sys.argv[2], sys.argv[3])
