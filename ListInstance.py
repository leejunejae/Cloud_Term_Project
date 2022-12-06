import boto3, os, re
from dotenv import load_dotenv

# 1

load_dotenv()

ec2 = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                     aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

instances = ec2.describe_instances()

set = {'ec2': []}

#print(instances)

for reservation in instances["Reservations"]:
    for instance in reservation["Instances"]:
        set['ec2'].append({
        "[id]": instance["InstanceId"],
        "[AMI]": instance["ImageId"],
        "[type]": instance["InstanceType"],
        "[state]": instance["State"]["Name"],
        "[monitoring state]": instance["Monitoring"]["State"]
        })

printlist = str(set)
printlist = re.sub(r"[^:\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)
print(printlist)