import boto3, os
from dotenv import load_dotenv
from botocore.exceptions import ClientError

#7

load_dotenv()

ec2 = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

instance_id=input()

try:
    response = ec2.reboot_instances(InstanceIds=[instance_id], DryRun=False)
    print('Success', response)
except ClientError as e:
    print('Error', e)