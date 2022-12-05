import boto3, os
from dotenv import load_dotenv
from boto3.session import Session

#4

load_dotenv()

ec2 = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

for region in ec2.describe_regions()['Regions']:
   print(region['RegionName'], region['Endpoint'])
