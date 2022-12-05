import boto3, os
from dotenv import load_dotenv


#6

load_dotenv()

ec2 = boto3.resource('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

image_id = input()

ec2.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType='t2.micro', )