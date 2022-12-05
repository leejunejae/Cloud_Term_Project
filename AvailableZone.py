import boto3, os
from dotenv import load_dotenv

# 2

load_dotenv()

ec2 = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

response = ec2.describe_availability_zones()
for zone in response['AvailabilityZones']:
    print(zone["ZoneId"])
    print(zone["RegionName"])
    print(zone["ZoneName"])
