import boto3
from botocore.exceptions import ClientError

REGION = "eu-north-1"
INSTANCE_TYPE = "t3.micro"  # якщо ти створив інший тип — впиши свій

def get_running_instances():
    ec2 = boto3.client("ec2", region_name=REGION)

    try:
        resp = ec2.describe_instances(
            Filters=[
                {"Name": "instance-state-name", "Values": ["running"]},
                {"Name": "instance-type", "Values": [INSTANCE_TYPE]},
            ]
        )

        reservations = resp.get("Reservations", [])
        if not reservations:
            print("[INFO] No running instances found with given filters.")
            return

        for r in reservations:
            for inst in r.get("Instances", []):
                instance_id = inst.get("InstanceId")
                instance_type = inst.get("InstanceType")
                public_ip = inst.get("PublicIpAddress")
                private_ip = inst.get("PrivateIpAddress")
                print(f"{instance_id}, {instance_type}, {public_ip}, {private_ip}")

    except ClientError as e:
        print(f"[ERROR] describe_instances failed: {e}")
        raise

if __name__ == "__main__":
    get_running_instances()
