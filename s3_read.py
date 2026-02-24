import boto3
import sys
from botocore.exceptions import ClientError

def read_object(bucket: str, key: str):
    s3 = boto3.client("s3")
    try:
        obj = s3.get_object(Bucket=bucket, Key=key)
        text = obj["Body"].read().decode("utf-8", errors="replace")
        print("[OK] Object content:\n")
        print(text)
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "NoSuchKey":
            print(f"[WARN] No such file: s3://{bucket}/{key}")
        else:
            print("[ERROR] get_object failed:", e)
            raise

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 s3_read.py <bucket> <key>")
        sys.exit(1)
    read_object(sys.argv[1], sys.argv[2])
