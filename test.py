import boto3, os, re, time
from flask import Flask, render_template, request
from dotenv import load_dotenv
from botocore.exceptions import ClientError

ssmclient = boto3.client('ssm', aws_access_key_id=os.getenv("AWS_ACCESS_KEY"),
                         aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"), )

instance_id = "i-03d2168006c51073a"

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

print(output)
