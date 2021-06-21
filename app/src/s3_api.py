import logging
import boto3
import os
from botocore.exceptions import ClientError
from typing import List, Union

IS_PROD = os.environ.get('AWS_ENV', 'test') == 'prod'


def get_s3_client(region: str = None):
    if IS_PROD:
        return boto3.client('s3')
    host = os.environ.get('LOCALSTACK_HOSTNAME', "localhost")

    return boto3.client('s3',
                        endpoint_url=f'http://{host}:4566',
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', 'test'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'test'),
                        region_name=os.environ.get('AWS_REGION', 'eu-central-1'))


def create_bucket(bucket_name: str, region: str = None) -> bool:
    try:
        if region is None:
            s3 = get_s3_client()
            s3.create(Bucket=bucket_name)
        else:
            s3 = get_s3_client(region=region)
            location = {'LocationConstraint': region}
            s3.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def delete_bucket(bucket_name: str, region: str = None) -> bool:
    try:
        s3 = get_s3_client(region="us")
        bucket_objects = list_objects(bucket_name)
        for obj in bucket_objects:
            s3.delete_object(Bucket=bucket_name, Key=obj['Key'])
        s3.delete_bucket(Bucket=bucket_name)
    except s3 as e:
        logging.error("Bucket is empty")
        logging.error(e)
        return False
    return True


def list_buckets() -> List[str]:
    try:
        s3_client = get_s3_client()
        buckets = [bucket["Name"] for bucket in s3_client.list()["Buckets"]]
    except (KeyError, ClientError) as e:
        logging.error(e)
        return []
    return buckets


def list_objects(bucket_name: str) -> List[dict]:
    try:
        s3 = get_s3_client()
        objects = s3.list_objects(Bucket=bucket_name)["Contents"]
    except (KeyError, ClientError) as e:
        logging.error(e)
        return []
    return objects


def delete_object(bucket_name: str, object_name: str) -> None:
    try:
        s3 = get_s3_client()
        bucket_objects = list_objects(bucket_name)
        for obj in bucket_objects:
            if obj['Key'] == object_name:
                s3.delete_object(Bucket=bucket_name, Key=object_name)
                return
    except (KeyError, ClientError) as e:
        logging.error(e)


def get_object_as_string(bucket_name: str, key: str) -> str:
    try:
        s3 = get_s3_client()
        obj = s3.get_object(Bucket=bucket_name, Key=key)
        string_object = obj['Body'].read().decode("utf-8")
    except (ClientError, UnicodeError, KeyError) as e:
        logging.error(e)
        return ""
    return string_object


def put_object(bucket_name: str, key: str, string_obj: str) -> bool:
    try:
        s3 = get_s3_client()
        obj = s3.put_object(Bucket=bucket_name, Key=key, Body=string_obj)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_presigned_post(bucket_name: str = 'Bucket', object_name: str = 'object.txt',
                          fields=None, conditions=None, expiration=3600) -> Union[dict, None]:
    """The response contains the presigned URL and required fields
       url = response['url']
       data = response['fields']
    """
    try:
        s3 = get_s3_client()
        response = s3.generate_presigned_post(Bucket=bucket_name,
                                              Key=object_name,
                                              Fields=fields,
                                              Conditions=conditions,
                                              ExpiresIn=expiration)
    except ClientError as e:
        logging.error(e)
        return

    return response
