import boto3, os
from dotenv import load_dotenv

#8

load_dotenv()

ec2 = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

images = ec2.describe_images(Owners=['self'])

for image in images['Images']:
    print(image['ImageId'], image['Name'], image['OwnerId'])