import boto3, os, re, time
from flask import Flask, render_template, request
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

ec2resource = boto3.resource('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                             aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )
ec2client = boto3.client('ec2', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                         aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )
ssmclient = boto3.client('ssm', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
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
    i = 1

    for reservation in instances["Reservations"]:
        for instance in reservation["Instances"]:
            set.append([
                "Information Instance " + str(i),
                "id : " + instance["InstanceId"],
                "AMI : " + instance["ImageId"],
                "type : " + instance["InstanceType"],
                "state : " + instance["State"]["Name"],
                "monitoring state : " + instance["Monitoring"]["State"] + " "
            ])
        i=i+1

    for instancestr in set:
        printlist = printlist + "[" + str(instancestr) + "]"
    printlist = re.sub(r"[^=:\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)

    return render_template("index.html", zone=printlist)


# 2
@app.route('/AvailableZone', methods=['GET'])
def AvailableZone():
    zones = ec2client.describe_availability_zones()
    set = []
    blank = "                      "
    for zone in zones['AvailabilityZones']:
        set.append([
            "id : " + zone["ZoneId"],
            "region : " + zone["RegionName"],
            "zone : " + zone["ZoneName"] + "\n"
        ])

    printlist = str(set)
    printlist = re.sub(r"[^\[\]=:\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)
    printlist = printlist[1:-1]

    return render_template("index.html", zone=printlist)


# 3
@app.route('/StartInstance', methods=['POST'])
def StartInstance():
    instance_id = request.form['zone']

    try:
        response = ec2client.start_instances(InstanceIds=[instance_id], DryRun=False)
        printlist = "Instance : " + str(response['StartingInstances'][0]['InstanceId']) + " is started"
        return render_template("index.html", zone=printlist)
    except ClientError as e:
        return render_template("index.html", zone="Error occur Please try again in a moment")

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
    printlist = re.sub(r"[^\[\]=:\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)
    printlist = printlist[1:-1]

    return render_template("index.html", zone=printlist)


# 5
@app.route('/StopInstance', methods=['POST'])
def StopInstance():
    instance_id = request.form['zone']

    try:
        response = ec2client.stop_instances(InstanceIds=[instance_id], DryRun=False)
        printlist = "Instance : " + str(response['StoppingInstances'][0]['InstanceId']) + " is stopped"
        return render_template("index.html", zone=printlist)
    except ClientError as e:
        return render_template("index.html", zone="Error occur Please try again in a moment")


# 6
@app.route('/CreateInstance', methods=['POST'])
def CreateInstance():
    image_id = request.form['zone']

    response = ec2resource.create_instances(ImageId=image_id, MinCount=1, MaxCount=1, InstanceType='t2.micro')
    printlist = str(response)
    printlist = printlist.replace("[ec2.Instance(id='", "")
    printlist = printlist.replace("')]", "")
    printlist = "New Instance " + printlist + " is created"
    return render_template("index.html", zone=printlist)


# 7
@app.route('/RebootInstance', methods=['POST'])
def RebootInstance():
    instance_id = request.form['zone']

    try:
        response = ec2client.reboot_instances(InstanceIds=[instance_id], DryRun=False)
        printlist = "Instance : " + instance_id + " is rebooted"
        return render_template("index.html", zone=printlist)
    except ClientError as e:
        return render_template("index.html", zone="Error occur Please try again in a moment")


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
    printlist = re.sub(r"[^\[\]=:\uAC00-\uD7A30-9a-zA-Z\s]", "", printlist)
    printlist = printlist[1:-1]

    return render_template("index.html", zone=printlist)

# 9
@app.route('/Condor_Status', methods=['POST'])
def Condor_Status():
    instance_id = request.form['zone']

    response = ssmclient.send_command(
        InstanceIds=[instance_id],
        DocumentName="AWS-RunShellScript",
        Parameters={'commands': ['condor_status']},
    )

    time.sleep(2)

    command_id = response['Command']['CommandId']
    output = ssmclient.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id,
    )

    return render_template("index.html", zone=output['StandardOutputContent'])

# 10
@app.route('/ModifyInstance', methods=['POST'])
def ModifyInstance():
    instance_id = request.form['zone']
    instance_type = request.form['value']
    instancestate = ec2client.describe_instances()
    set = []

    for reservation in instancestate["Reservations"]:
        for instance in reservation["Instances"]:
            set.append([
                instance["InstanceId"],
                instance["State"]["Name"]
            ])

    find_index = [i for i in range(len(set)) if instance_id in set[i]]
    indexint = int(find_index[0])

    try:
        if set[indexint][1] == "running":
            ec2client.stop_instances(InstanceIds=[instance_id], DryRun=False)
            waiter = ec2client.get_waiter('instance_stopped')
            waiter.wait(InstanceIds=[instance_id])
        ec2client.modify_instance_attribute(InstanceId=instance_id, Attribute='instanceType', Value=instance_type)
        printlist = "Instance : " + instance_id + "\'s type is modified"
        return render_template("index.html", zone=printlist)
    except ClientError as e:
        return render_template("index.html", zone="Error occur Please try again in a moment")


if __name__ == '__main__':
    app.run()
