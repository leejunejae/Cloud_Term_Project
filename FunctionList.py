import boto3, os, re
from flask import Flask, render_template, request
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

ec2resource = boto3.resource('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                             aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )
ec2client = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                         aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


# 1
@app.route('/ListInstance', methods=['GET'])
def ListInstance(zone=None):
    instances = ec2client.describe_instances()
    set = []
    printlist = ""

    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            set.append([
                "id : " + instance["InstanceId"],
                "AMI : " + instance["ImageId"],
                "type : " + instance["InstanceType"],
                "state : " + instance["State"]["Name"],
                "monitoring state : " + instance["Monitoring"]["State"]
            ])

    for instancestr in set:
        printlist = printlist + "[" + str(instancestr) + "]"
    printlist = re.sub(r"[^=:\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)

    return render_template("index.html", zone=printlist)


# 2
@app.route('/AvailableZone', methods=['GET'])
def AvailableZone():
    zones = ec2client.describe_availability_zones()
    set = []
    for zone in zones['AvailabilityZones']:
        set.append([
            "id" + zone["ZoneId"],
            "region" + zone["RegionName"],
            "zone" + zone["ZoneName"],
        ])

    printlist = str(set)
    printlist = re.sub(r"[^=:,\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)

    return render_template("index.html", zone=printlist)


# 3
@app.route('/StartInstance', methods=['POST'])
def StartInstance():
    instance_id = request.form['zone']

    try:
        response = ec2client.start_instances(InstanceIds=[instance_id], DryRun=False)
        return render_template("index.html", zone=response['StartingInstances'][0]['InstanceId'])
    except ClientError as e:
        return render_template("index.html", zone=response)

# 4
@app.route('/AvailableRegions', methods=['GET'])
def AvailableRegions():
    regions = ec2client.describe_regions()
    set = []
    for region in regions['Regions']:
        set.append([
            "region : " + region['RegionName'],
            "endpoint : " + region['Endpoint']
        ])
    printlist = str(set)
    printlist = re.sub(r"[^=:,\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)

    return render_template("index.html", zone=printlist)


# 5
@app.route('/StopInstance', methods=['POST'])
def StopInstance():
    instance_id = request.form['zone']

    try:
        response = ec2client.start_instances(InstanceIds=[instance_id], DryRun=False)
        return render_template("index.html", zone=response['StoppingInstances'][0]['InstanceId'])
    except ClientError as e:
        return render_template("index.html", zone=response)


# 6
@app.route('/CreateInstance', methods=['POST'])
def CreateInstance():
    image_id = request.form['zone']

    response = ec2resource.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType='t2.micro')
    printlist = str(response)
    printlist = printlist.replace("[ec2.Instance(id='", "")
    printlist = printlist.replace("')]", "")
    return render_template("index.html", zone=printlist)


# 7
@app.route('/RebootInstance', methods=['POST'])
def RebootInstance():
    instance_id = request.form['zone']

    try:
        response = ec2client.reboot_instances(InstanceIds=[instance_id], DryRun=False)
        return render_template("index.html", zone=instance_id)
    except ClientError as e:
        return render_template("index.html", zone=response)


# 8
@app.route('/ListImages', methods=['GET'])
def ListImages():
    images = ec2client.describe_images(Owners=['self'])
    set = []
    for image in images['Images']:
        set.append([
            "ImageID : " + image['ImageId'],
            "Name : " + image['Name'],
            "Owner : " + image['OwnerId']
        ])

    printlist = str(set)
    printlist = re.sub(r"[^=:,\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)

    return render_template("index.html", zone=printlist)


if __name__ == '__main__':
    app.run()
