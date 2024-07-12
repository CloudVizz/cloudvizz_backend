import boto3

def get_session(creds, region):
    return boto3.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken'],
        region_name=region
    )

def list_ec2_instances(session):
    ec2_client = session.client('ec2')
    response = ec2_client.describe_instances()
    instances = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append({
                'ResourceType': 'EC2',
                'InstanceId': instance['InstanceId'],
                'InstanceType': instance['InstanceType'],
                'State': instance['State']['Name'],
                'Region': session.region_name
            })
    return instances

def list_s3_buckets(session):
    s3_client = session.client('s3')
    response = s3_client.list_buckets()
    buckets = []
    for bucket in response['Buckets']:
        buckets.append({
            'ResourceType': 'S3',
            'BucketName': bucket['Name'],
            'CreationDate': bucket['CreationDate'].strftime("%Y-%m-%d %H:%M:%S"),
            'Region': session.region_name
        })
    return buckets

def list_vpcs(session):
    ec2_client = session.client('ec2')
    response = ec2_client.describe_vpcs()
    vpcs = []
    for vpc in response['Vpcs']:
        vpcs.append({
            'ResourceType': 'VPC',
            'VpcId': vpc['VpcId'],
            'State': vpc['State'],
            'Region': session.region_name
        })
    return vpcs

def list_subnets(session):
    ec2_client = session.client('ec2')
    response = ec2_client.describe_subnets()
    subnets = []
    for subnet in response['Subnets']:
        subnets.append({
            'ResourceType': 'Subnet',
            'SubnetId': subnet['SubnetId'],
            'VpcId': subnet['VpcId'],
            'State': subnet['State'],
            'Region': session.region_name
        })
    return subnets

def list_security_groups(session):
    ec2_client = session.client('ec2')
    response = ec2_client.describe_security_groups()
    security_groups = []
    for sg in response['SecurityGroups']:
        security_groups.append({
            'ResourceType': 'SecurityGroup',
            'GroupId': sg['GroupId'],
            'GroupName': sg['GroupName'],
            'VpcId': sg.get('VpcId'),
            'Region': session.region_name
        })
    return security_groups

def get_all_regions():
    ec2_client = boto3.client('ec2')
    regions = ec2_client.describe_regions()
    return [region['RegionName'] for region in regions['Regions']]

def list_all_resources(creds):
    resources = []
    for region in get_all_regions():
        session = get_session(creds, region)
        resources.extend(list_ec2_instances(session))
        resources.extend(list_s3_buckets(session))
        resources.extend(list_vpcs(session))
        resources.extend(list_subnets(session))
        resources.extend(list_security_groups(session))
    return resources

def get_resource_details(creds, region, resource_id, resource_type):
    session = get_session(creds, region)
    ec2_client = session.client('ec2')

    if resource_type == 'EC2':
        response = ec2_client.describe_instances(InstanceIds=[resource_id])
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                return {
                    'ResourceType': 'EC2',
                    'InstanceId': instance['InstanceId'],
                    'InstanceType': instance['InstanceType'],
                    'State': instance['State']['Name'],
                    'Region': session.region_name,
                    'Details': instance
                }

    elif resource_type == 'S3':
        s3_client = session.client('s3')
        response = s3_client.get_bucket_location(Bucket=resource_id)
        return {
            'ResourceType': 'S3',
            'BucketName': resource_id,
            'Region': response['LocationConstraint']
        }

    elif resource_type == 'VPC':
        response = ec2_client.describe_vpcs(VpcIds=[resource_id])
        for vpc in response['Vpcs']:
            return {
                'ResourceType': 'VPC',
                'VpcId': vpc['VpcId'],
                'State': vpc['State'],
                'Region': session.region_name,
                'Details': vpc
            }

    elif resource_type == 'Subnet':
        response = ec2_client.describe_subnets(SubnetIds=[resource_id])
        for subnet in response['Subnets']:
            return {
                'ResourceType': 'Subnet',
                'SubnetId': subnet['SubnetId'],
                'VpcId': subnet['VpcId'],
                'State': subnet['State'],
                'Region': session.region_name,
                'Details': subnet
            }

    elif resource_type == 'SecurityGroup':
        response = ec2_client.describe_security_groups(GroupIds=[resource_id])
        for sg in response['SecurityGroups']:
            return {
                'ResourceType': 'SecurityGroup',
                'GroupId': sg['GroupId'],
                'GroupName': sg['GroupName'],
                'VpcId': sg.get('VpcId'),
                'Region': session.region_name,
                'Details': sg
            }

    return None
