import boto3
import sys
from botocore.exceptions import ClientError

REGION = "eu-north-1"

def get_state(ec2, instance_id: str) -> str:
    resp = ec2.describe_instances(InstanceIds=[instance_id])
    return resp["Reservations"][0]["Instances"][0]["State"]["Name"]

def start_instance(instance_id: str):
    ec2 = boto3.client("ec2", region_name=REGION)

    try:
        state = get_state(ec2, instance_id)
        print(f"[INFO] Current state: {state}")

        if state == "running":
            print("[OK] Instance already running. Nothing to do.")
            return

        if state == "stopped":
            print("[INFO] Starting instance...")
            ec2.start_instances(InstanceIds=[instance_id])

            waiter = ec2.get_waiter("instance_running")
            waiter.wait(InstanceIds=[instance_id])

            print("[OK] Instance is now RUNNING")
            state = get_state(ec2, instance_id)
            print(f"[INFO] New state: {state}")
            return

        if state in ("terminated", "shutting-down"):
            print("[ERROR] Instance is terminated/shutting-down. It cannot be started. Create a new one (restore).")
            return

        # stopping/pending/other
        print(f"[WARN] Instance is in state '{state}'. Wait until it becomes 'stopped' then start again.")

    except ClientError as e:
        print("[ERROR] start flow failed:", e)
        raise

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 ec2_start.py <instance-id>")
        sys.exit(1)

    start_instance(sys.argv[1])
