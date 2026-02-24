import boto3
from botocore.exceptions import ClientError

REGION = "eu-north-1"
INSTANCE_TYPE = "t3.micro"      # safe для Free Tier (часто). Якщо у тебе дозволено інше — зміниш.
KEY_NAME = "ec2-keypair"
INSTANCE_NAME = "demo"

SSM_PARAM = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-default-x86_64"

def get_latest_ami_id():
    ssm = boto3.client("ssm", region_name=REGION)
    return ssm.get_parameter(Name=SSM_PARAM)["Parameter"]["Value"]

def create_instance():
    ec2 = boto3.client("ec2", region_name=REGION)
    ami_id = get_latest_ami_id()
    print(f"[INFO] Using AMI: {ami_id}")

    try:
        resp = ec2.run_instances(
            ImageId=ami_id,
            MinCount=1,
            MaxCount=1,
            InstanceType=INSTANCE_TYPE,
            KeyName=KEY_NAME,
            TagSpecifications=[{
                "ResourceType": "instance",
                "Tags": [{"Key": "Name", "Value": INSTANCE_NAME}],
            }],
        )
        instance_id = resp["Instances"][0]["InstanceId"]
        print(f"[OK] Instance created: {instance_id}")
        return instance_id

    except ClientError as e:
        print(f"[ERROR] Failed to create instance: {e}")
        raise

if __name__ == "__main__":
    create_instance()
