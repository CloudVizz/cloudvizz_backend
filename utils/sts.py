import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from config import Config

def assume_role(account_id, role_name, external_id):
    try:
        sts_client = boto3.client(
            'sts',
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY
        )
        
        role_arn = f"arn:aws:iam::{account_id}:role/{role_name}"
        response = sts_client.assume_role(
            RoleArn=role_arn,
            RoleSessionName='AssumeRoleSession',
            ExternalId=external_id
        )
        
        credentials = response['Credentials']
        return {
            'AccessKeyId': credentials['AccessKeyId'],
            'SecretAccessKey': credentials['SecretAccessKey'],
            'SessionToken': credentials['SessionToken']
        }
    except NoCredentialsError:
        raise Exception("No AWS credentials found.")
    except PartialCredentialsError:
        raise Exception("Incomplete AWS credentials found.")
    except Exception as e:
        raise Exception(f"Error assuming role: {str(e)}")
