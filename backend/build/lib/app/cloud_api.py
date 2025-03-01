import boto3
from fastapi import HTTPException
import json
from fastapi import File
import uuid


DEFAULT_REGION = "us-east-1"

boto_session = boto3.Session(
    profile_name="resoursphere",region_name=DEFAULT_REGION
)
ec2 = boto_session.client('ec2')
s3 = boto_session.client('s3')
route53 = boto_session.client('route53')

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

def construct_bucket_url(bucket_name: str) -> str:
    return f"https://{bucket_name}.s3.amazonaws.com"

def create_s3_bucket(name: str, user: str, public: bool = False) -> dict:
    try:
        # Create the S3 bucket
        response = s3.create_bucket(
            Bucket=name,
            # CreateBucketConfiguration={
            #     'LocationConstraint': DEFAULT_REGION
            # }
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
            # Remove Block Public Access settings
            s3.put_public_access_block(
                Bucket=name,
                PublicAccessBlockConfiguration={
                    'BlockPublicAcls': False,
                    'IgnorePublicAcls': False,
                    'BlockPublicPolicy': False,
                    'RestrictPublicBuckets': False
                }
            )
            
            # Apply a public bucket policy
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
        # Wait until the bucket exists and is accessible
        waiter = s3.get_waiter('bucket_exists')
        waiter.wait(Bucket=name)
        
        return {
            "bucket_name": name,
            "status": "created",
            "bucket_url": construct_bucket_url(name)
        }
    except s3.exceptions.ClientError as e:
        error_code = e.response['Error']['Code']
        if error_code == 'BucketAlreadyExists' or error_code == 'BucketAlreadyOwnedByYou':
            raise HTTPException(
                status_code=409,
                detail=f"Bucket {name} already exists"
            )
        else:
            raise HTTPException(
                status_code=500,
                detail=f"API Error: {e}"
            )


def get_s3_buckets(user: str = None) -> list[dict]:
    # Get all buckets first
    response = s3.list_buckets()
    
    buckets = []
    for bucket in response['Buckets']:
        try:
            # Get tags for each bucket
            tags = s3.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']
            
            # Check if bucket matches our filters
            managed_by_resoursphere = False
            owned_by_user = False
            
            for tag in tags:
                if tag['Key'] == 'ManagedBy' and tag['Value'] == 'ResourSphere':
                    managed_by_resoursphere = True
                if tag['Key'] == 'Owner' and tag['Value'] == user:
                    owned_by_user = True
            
            # Only include bucket if it matches our filters
            if managed_by_resoursphere and (not user or owned_by_user):
                bucket_description = {
                    "name": bucket['Name'],
                    "url": construct_bucket_url(bucket['Name'])
                }
                buckets.append(bucket_description)
                
        except s3.exceptions.ClientError as e:
            # Skip buckets where we can't read tags
            continue
            
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
    except s3.exceptions.NoSuchBucket as e:
        raise HTTPException(
            status_code=404,
            detail=f"Bucket {bucket_name} does not exist."
        )
    except s3.exceptions.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting bucket: {e}"
        )


def upload_file_to_s3_bucket(bucket_name: str, file: File) -> dict:
    try:
        file.file.seek(0)
        s3.upload_fileobj(file.file, bucket_name, file.filename)
        return {
            "bucket_name": bucket_name,
            "file_name": file.filename,
            "status": "uploaded"
        }
    except s3.exceptions.ClientError as e:
        raise HTTPException(
            status_code=500, detail=f"AWS API returned error: {e}"
        )


def create_dns_zone(name: str, user: str) -> dict:
    try:
        # Create the hosted zone
        response = route53.create_hosted_zone(
            Name=name,
            CallerReference=str(uuid.uuid4()),
            HostedZoneConfig={
                'Comment': 'Managed by ResourSphere',
            },
        )
        
        # Extract the hosted zone ID and remove the prefix
        zone_id = response['HostedZone']['Id'].split('/')[-1]
        
        # Add tags to the hosted zone
        route53.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id,
            AddTags=[
                {
                    'Key': 'ManagedBy',
                    'Value': 'ResourSphere'
                },
                {
                    'Key': 'Owner',
                    'Value': user
                }
            ]
        )
        
        return {
            "zone_id": zone_id,
            "name": name,
            "status": "created"
        }
    except route53.exceptions.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"AWS API Error: {e}"
        )


def delete_dns_zone(zone_id: str) -> dict:
    try:
        route53.delete_hosted_zone(Id=zone_id)
        return {
            "zone_id": zone_id,
            "status": "deleted"
        }
    except route53.exceptions.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"AWS API Error: {e}"
        )

def get_dns_zones_list(user: str=None) -> list[dict]:
    try:
        # Get all hosted zones
        response = route53.list_hosted_zones()
        zones = []
        
        # Process each zone to check tags
        for zone in response['HostedZones']:
            zone_id = zone['Id'].split('/')[-1]
            
            # Get tags for this zone
            tags_response = route53.list_tags_for_resource(
                ResourceType='hostedzone',
                ResourceId=zone_id
            )
            
            tags = {tag['Key']: tag['Value'] for tag in tags_response['ResourceTagSet']['Tags']}
            
            # Check if zone is managed by ResourSphere
            if tags.get('ManagedBy') == 'ResourSphere':
                # If user is specified, check owner tag
                if user is None or tags.get('Owner') == user:
                    zones.append({
                        "zone_id": zone_id,
                        "name": zone['Name'],
                        # "tags": tags
                    })
        
        return zones
    except route53.exceptions.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"AWS API Error while asking for list of zones: {e}"
        )
def create_dns_record(zone_id: str, name: str, type: str, value: str) -> dict:
    try:
        response = route53.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': name,
                            'Type': type,
                            'TTL': 300
                        },

                        'ResourceRecords': [{'Value': value}]
                    }
                ]
            }
        )
        return {
            "zone_id": zone_id,
            "name": name,
            "type": type,
            "value": value,
            "status": "created"
        }
    except route53.exceptions.ClientError as e:
        raise HTTPException(
            status_code=500,
            detail=f"AWS API Error: {e}"
        )

