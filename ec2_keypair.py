import boto3
import os
from botocore.exceptions import ClientError

REGION = "eu-north-1"
KEY_NAME = "ec2-keypair"          # назва ключа в AWS
KEY_PATH = "./aws_ec2_key.pem"    # куди збережемо локально

def create_key_pair():
    ec2 = boto3.client("ec2", region_name=REGION)

    try:
        response = ec2.create_key_pair(KeyName=KEY_NAME)
        private_key = response["KeyMaterial"]

        # записуємо файл і ставимо права 400 (Linux/macOS)
        with os.fdopen(os.open(KEY_PATH, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o400), "w") as f:
            f.write(private_key)

        print(f"[OK] Key pair created: {KEY_NAME}")
        print(f"[OK] Private key saved to: {KEY_PATH} (mode 400)")

    except ClientError as e:
        code = e.response["Error"]["Code"]

        if code == "InvalidKeyPair.Duplicate":
            print(f"[WARN] Key pair '{KEY_NAME}' already exists in AWS. Nothing to create.")
        else:
            print(f"[ERROR] Failed to create key pair: {e}")
            raise

if __name__ == "__main__":
    create_key_pair()
