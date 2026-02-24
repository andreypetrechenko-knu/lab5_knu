import boto3
import sys
from botocore.exceptions import ClientError

REGION = "eu-north-1"

def terminate_instance(instance_id: str):
    ec2 = boto3.client("ec2", region_name=REGION)
    try:
        resp = ec2.terminate_instances(InstanceIds=[instance_id])
        print(resp)
    except ClientError as e:
        print(f"[ERROR] terminate_instances failed: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ec2_terminate.py <instance-id>")
        sys.exit(1)
    terminate_instance(sys.argv[1])
