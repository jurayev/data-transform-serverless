import logging
import boto3
import os
from botocore.exceptions import ClientError

IS_PROD = os.environ['AWS_ENV'] == 'prod' if 'AWS_ENV' in os.environ else False

def get_s3_client(region:str=None):
    if IS_PROD:
        return boto3.client('s3')
    HOST = os.environ['LOCALSTACK_HOSTNAME'] if 'LOCALSTACK_HOSTNAME' in os.environ else "localhost"
    return boto3.client('s3', 
                        endpoint_url=f'http://{HOST}:4566',
                        aws_access_key_id=os.environ['AWS_ACCESS_KEY_ID'],
                        aws_secret_access_key=os.environ['AWS_SECRET_ACCESS_KEY'],
                        region_name=os.environ['AWS_REGION'])

def create_bucket(bucket_name, region=None) -> bool:
    try:
        if region is None:
            s3 = get_s3_client()
            s3.create_bucket(Bucket=bucket_name)
        else:
            s3 = get_s3_client(region=region)
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def delete_bucket(bucket_name:str, region:str=None) -> bool:
    try:
        s3 = get_s3_client(region=region)
        bucket_objects = list_objects(bucket_name)
        for obj in bucket_objects:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key']) 
        s3.delete_bucket(Bucket=bucket_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True

def list_buckets() -> list:
    try:
        s3_client = get_s3_client()
        buckets = [bucket["Name"] for bucket in s3_client.list_buckets()["Buckets"]]
    except (KeyError, ClientError) as e:
        logging.error(e)
        return []
    return buckets


def list_objects(bucket_name:str):
    try:
        s3 = get_s3_client()
        objects = s3.list_objects_v2(Bucket=bucket_name)["Contents"]
    except (KeyError, ClientError) as e:
        logging.error(e)
        return []
    return objects

def delete_object(bucket_name:str, object_name:str) -> None:
    try:
        s3 = get_s3_client()
        bucket_objects = list_objects(bucket_name)
        for obj in bucket_objects:
            if obj['Key'] == object_name:
                s3.delete_object(Bucket=bucket_name, Key=object_name)
                return
    except ClientError as e:
        logging.error(e)


def get_object_as_string(bucket_name:str, key:str) -> str:
    try:
        s3 = get_s3_client()
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        string_object = obj["Body"].read().decode('utf-8')
    except ClientError as e:
        logging.error(e)
        return ""
    return string_object

def put_object(bucket_name:str, key:str, string_obj:str) -> bool:
    try:
        s3 = get_s3_client()
        obj = s3.put_object(Bucket=bucket_name, Key=key, Body=string_obj)
    except ClientError as e:
        logging.error(e)
        return False
    return True
