import boto3, os
from dotenv import load_dotenv

# 1

load_dotenv()

ec2 = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(instance["InstanceId"])
        print(instance["ImageId"])
        print(instance["InstanceType"])
        print(instance["State"]["Name"])
        print(instance["Monitoring"])
