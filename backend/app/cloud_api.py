import boto3
from fastapi import HTTPException
import json


DEFAULT_REGION = "us-east-1"

boto_session = boto3.Session(
    profile_name="resoursphere",region_name=DEFAULT_REGION
)
ec2 = boto_session.client('ec2')
s3 = boto_session.client('s3')
DEFAULT_VPC_ID = "vpc-08879d17f5e284b80"
DEFAULT_SUBNET_ID = "subnet-07d6bb7b15ccc8452"

def launch_ec2_instance(name: str, instance_type: str, ami: str, user: str) -> dict:
    
    # Create tags for the instance
    tags = [
        {
            'Key': 'Name',
            'Value': name
        },
        {
            'Key': 'Owner',
            'Value': user
        },
        {
            'Key': 'ManagedBy',
            'Value': 'ResourSphere'
        }
    ]
    
    # Launch the EC2 instance
    response = ec2.run_instances(
        ImageId=ami,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        SubnetId=DEFAULT_SUBNET_ID,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': tags
            }
        ]
    )
    
    instance = response['Instances'][0]
    instance_id = instance['InstanceId']
    
    # Wait for the instance to be running and have a public IP
    waiter = ec2.get_waiter('instance_running')
    waiter.wait(InstanceIds=[instance_id])
    
    # Get the public IP address
    instance_info = ec2.describe_instances(InstanceIds=[instance_id])
    public_ip = instance_info['Reservations'][0]['Instances'][0]['PublicIpAddress']
    
    return {
        "instance_id": instance_id,
        "public_ip": public_ip
    }

def terminate_ec2_instance(instance_id: str, user: str) -> dict:
    # Verify the instance exists
    filters = [
        {
            'Name': 'instance-id',
            'Values': [instance_id]
        },
        # {
        #     'Name': 'tag:Owner',
        #     'Values': [user]
        # },
        {
            'Name': 'tag:ManagedBy',
            'Values': ['ResourSphere']
        }
    ]
    
    response = ec2.describe_instances(Filters=filters)
    
    if not response['Reservations']:
        raise ValueError(f"Instance not found")
    # Check if the instance is already terminated
    # instance_state = response['Reservations'][0]['Instances'][0]['State']['Name']
    # if instance_state == 'terminated':
    #     return {
    #         "instance_id": instance_id,
    #         "status": "already terminated"
    #     }

    # Terminate the instance
    ec2.terminate_instances(InstanceIds=[instance_id])
    
    # Wait for the instance to be terminated
    waiter = ec2.get_waiter('instance_terminated')
    waiter.wait(InstanceIds=[instance_id])
    
    return {
        "instance_id": instance_id,
        "status": "terminated"
    }

def get_ec2_instances_by_user(user: str, state: str = None) -> list[dict]:
    filters =[
        {
            'Name': 'tag:Owner',
            'Values': [user]
        },
        {
            'Name': 'tag:ManagedBy',
            'Values': ['ResourSphere']
        }
    ]

    if state:
        filters.append({
            'Name': 'instance-state-name',
            'Values': [state]
        })

    response = ec2.describe_instances(Filters=filters)
    
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instance_info = {
                "instance_id": instance['InstanceId'],
                "public_ip": instance.get('PublicIpAddress', 'N/A'),
                "name": next((tag['Value'] for tag in instance['Tags'] if tag['Key'] == 'Name'), '[No Name]'),
                "state": instance['State']['Name']
            }
            instances.append(instance_info)
    
    return instances

def start_ec2_instance(instance_id: str) -> dict:
    try:
        ec2.start_instances(InstanceIds=[instance_id])
        
        # Wait for the instance to be running
        waiter = ec2.get_waiter('instance_running')
        waiter.wait(InstanceIds=[instance_id])
        
        return {
            "instance_id": instance_id,
            "status": "started"
        }
    except ec2.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
            raise HTTPException(
                status_code=404,
                detail=f"API Error: Instance {instance_id} not found"
            )
        else:
            raise HTTPException(status_code=500, detail=f"API Error: {e}")

def stop_ec2_instance(instance_id: str) -> dict:
    # Check if instance exists
    # try:
    #     ec2.describe_instances(InstanceIds=[instance_id])
    # except ec2.exceptions.ClientError as e:
    #     if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
    #         raise HTTPException(
    #             status_code=404,
    #             detail=f"API Error: Instance {instance_id} not found"
    #         )
    try:
        ec2.stop_instances(InstanceIds=[instance_id])
        # Wait for the instance to be stopped
        waiter = ec2.get_waiter('instance_stopped')
        waiter.wait(InstanceIds=[instance_id])
        
        return {
            "instance_id": instance_id,
            "status": "stopped"
        }
    except ec2.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidInstanceID.NotFound':
            raise HTTPException(
                status_code=404,
                detail=f"API Error: Instance {instance_id} not found"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"API Error: {e}"
            )

def create_s3_bucket(name: str, user: str, public: bool = False) -> dict:
    try:
        # Create the S3 bucket
        response = s3.create_bucket(
            Bucket=name,
            CreateBucketConfiguration={
                'LocationConstraint': DEFAULT_REGION
            }
        )
        
        # Add tags to the bucket
        tagging = {
            'TagSet': [
                {
                    'Key': 'ManagedBy',
                    'Value': 'ResourSphere'
                },
                {
                    'Key': 'Owner',
                    'Value': user 
                }
            ]
        }
        s3.put_bucket_tagging(
            Bucket=name,
            Tagging=tagging
        )
        
        # If public access is requested, update the bucket policy
        if public:
            bucket_policy = {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Sid": "PublicReadGetObject",
                        "Effect": "Allow",
                        "Principal": "*",
                        "Action": "s3:GetObject",
                        "Resource": f"arn:aws:s3:::{name}/*"
                    }
                ]
            }
            s3.put_bucket_policy(
                Bucket=name,
                Policy=json.dumps(bucket_policy)
            )
        
        return {
            "bucket_name": name,
            "status": "created",
        }
    except s3.exceptions.BucketAlreadyExists as e:
        raise HTTPException(
            status_code=409,
            detail=f"Bucket {name} already exists"
        )
    except s3.exceptions.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"API Error: {e}"
        )
    
def get_s3_buckets_for_user(user: str) -> list[dict]:
    filters = [
        {
            'Name': 'tag:Owner',
            'Values': [user]
        },  
        {
            'Name': 'tag:ManagedBy',
            'Values': ['ResourSphere']
        }
    ]
    
    response = s3.list_buckets(Filters=filters)
    
    buckets = []
    for bucket in response['Buckets']:
        bucket_description = {"name": bucket['Name']}
        buckets.append(bucket_description)
    return buckets

def delete_s3_bucket(bucket_name: str) -> dict:
    try:
        s3.delete_bucket(Bucket=bucket_name)
        
        # Wait until the bucket is deleted
        waiter = s3.get_waiter('bucket_not_exists')
        waiter.wait(Bucket=bucket_name)
        
        return {
            "bucket_name": bucket_name,
            "status": "deleted"
        }
    except s3.exceptions.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting bucket: {e}"
        )
