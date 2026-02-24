import boto3
import sys
from botocore.exceptions import ClientError

def delete_bucket(bucket: str):
    s3 = boto3.client("s3")
    try:
        s3.delete_bucket(Bucket=bucket)
        print(f"[OK] Deleted bucket: {bucket}")
    except ClientError as e:
        code = e.response["Error"]["Code"]
        if code == "BucketNotEmpty":
            print(f"[WARN] Bucket is not empty: {bucket}. Delete objects first.")
        else:
            print("[ERROR] delete_bucket failed:", e)
            raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 s3_delete_bucket.py <bucket>")
        sys.exit(1)
    delete_bucket(sys.argv[1])
