import boto3

def assume_role(account_id, role_name, external_id):
    # Create an STS client
    sts_client = boto3.client('sts')
    print("assume role")
    
    # Construct the role ARN
    role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
    
    # Assume the role
    response = sts_client.assume_role(
        RoleArn=role_arn,
        RoleSessionName='AssumeRoleSession',
        ExternalId=external_id
    )
    
    # Extract the temporary security credentials
    credentials = response['Credentials']
    print(credentials)
    
    return {
        'AccessKeyId': credentials['AccessKeyId'],
        'SecretAccessKey': credentials['SecretAccessKey'],
        'SessionToken': credentials['SessionToken']
    }

def list_ec2_instances(creds):
    # Use the assumed role credentials to create a session
    session = boto3.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken'],
        region_name='ap-south-1'
    )
    
    # Create an EC2 client using the session
    ec2_client = session.client('ec2')
    
    # Describe EC2 instances
    response = ec2_client.describe_instances()
    
    # Print the response
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            print(f"Instance ID: {instance['InstanceId']}")
            print(f"Instance Type: {instance['InstanceType']}")
            print(f"State: {instance['State']['Name']}")
            print("-----")

def list_tagged_resources(creds):
    # Create a session using AWS credentials and region
    session = boto3.Session(
        aws_access_key_id=creds['AccessKeyId'],
        aws_secret_access_key=creds['SecretAccessKey'],
        aws_session_token=creds['SessionToken'],
        region_name='ap-south-1'
    )
    

    # Create a client for the Resource Groups Tagging API
    tagging_client = session.client('resourcegroupstaggingapi')

    # Get all tagged resources
    response = tagging_client.get_resources(
        ResourceTypeFilters=['ec2:instance']
    )
    # print(response)

    # Parse and print instance information
    instances = []
    for resource_tag_mapping in response['ResourceTagMappingList']:
        resource_arn = resource_tag_mapping['ResourceARN']
        tags = resource_tag_mapping.get('Tags', [])
        
        # Create a dictionary of the tags
        tag_dict = {tag['Key']: tag['Value'] for tag in tags}
        
        instances.append({
            'Resource ARN': resource_arn,
            'Tags': tag_dict
        })

    return instances

def main():
    account_id = 381491871778
    role_name = "cv"
    external_id = "cloudvizz"

    try:
        # Assume the role
        creds = assume_role(account_id, role_name, external_id)
        
        # List EC2 instances
        list_ec2_instances(creds)
        print("\n")
        instances = list_tagged_resources(creds)
        for idx, instance in enumerate(instances, start=1):
            print(f"Instance {idx}:")
            print(f"  Resource ARN: {instance['Resource ARN']}")
            for tag_key, tag_value in instance['Tags'].items():
                print(f"  {tag_key}: {tag_value}")
            print()
        
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == '__main__':
    main()
