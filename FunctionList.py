import boto3, os
from flask import Flask,render_template
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

ec2resource = boto3.resource('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                             aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )
ec2client = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                   aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )


# 1
def ListInstance():
    response = ec2client.describe_instances()
    set = []

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            set.append({
                "[id]": instance["InstanceId"],
                "[AMI]": instance["ImageId"],
                "[type]": instance["InstanceType"],
                "[state]": instance["State"]["Name"],
                "[monitoring state]": instance["Monitoring"]
            })

    return set

# 2
def AvailableZone():
    response = ec2client.describe_availability_zones()
    for zone in response['AvailabilityZones']:
        print(zone["ZoneId"])
        print(zone["RegionName"])
        print(zone["ZoneName"])


# 3
def StartInstance():
    instance_id = input()

    try:
        ec2client.start_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    try:
        response = ec2client.start_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)


# 4
def AvailableRegions():
    for region in ec2client.describe_regions()['Regions']:
        print(region['RegionName'], region['Endpoint'])


# 5
def StopInstance():
    instance_id = input()

    try:
        ec2client.stop_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            raise

    # Dry run succeeded, call stop_instances without dryrun
    try:
        response = ec2client.stop_instances(InstanceIds=[instance_id], DryRun=False)
        print(response)
    except ClientError as e:
        print(e)


# 6
def CreateInstance():
    image_id = input()

    ec2resource.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType='t2.micro', )
# 7
def RebootInstance():
    instance_id = input()

    try:
        ec2client.reboot_instances(InstanceIds=[instance_id], DryRun=True)
    except ClientError as e:
        if 'DryRunOperation' not in str(e):
            print("You don't have permission to reboot instances.")
            raise

    try:
        response = ec2client.reboot_instances(InstanceIds=[instance_id], DryRun=False)
        print('Success', response)
    except ClientError as e:
        print('Error', e)
# 8
def ListImages():
    images = ec2client.describe_images(Owners=['self'])

    for image in images['Images']:
        print(image['ImageId'], image['Name'], image['OwnerId'])

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()