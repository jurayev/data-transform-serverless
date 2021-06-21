import logging
import boto3
import os
from botocore.exceptions import ClientError
from typing import Union, List

IS_PROD = os.environ.get('AWS_ENV', 'test') == 'prod'


def get_dynamodb():
    if IS_PROD:
        return boto3.resource('dynamodb')
    host = os.environ.get('LOCALSTACK_HOSTNAME', "localhost")
    return boto3.resource('dynamodb',

                          aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', 'test'),
                          aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'test'),
                          region_name=os.environ.get('AWS_REGION', 'eu-central-1'))


def get_dynamodb_client():
    if IS_PROD:
        return boto3.resource('dynamodb')
    host = os.environ.get('LOCALSTACK_HOSTNAME', "localhost")

    return boto3.client('dynamodb',
                        endpoint_url=f'http://{host}:4566',
                        aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID', 'test'),
                        aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY', 'test'),
                        region_name=os.environ.get('AWS_REGION', 'eu-central-1'))


def get_rules(rule_id: int = 1, table: str = "rulesTable") -> Union[dict, None]:
    dynamodb = get_dynamodb()
    table = dynamodb.Table(table)

    try:
        response = table.get_item(Key={'RuleId': rule_id})
    except ClientError as e:
        logging.error(e.response['Error']['Message'])
    else:
        return response.get('Item', None)


def create_rules_table(table_name: str = "rulesTable") -> dict:
    dynamodb = get_dynamodb()

    table = dynamodb.create_tb(
        TableName=table_name,
        KeySchema=[
            {
                'AttributeName': 'RuleId',
                'KeyType': 'HASH'  # Partition key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'RuleId',
                'AttributeType': 'N'
            }
        ]
    )
    return table


def put_rule() -> dict:
    dynamodb = get_dynamodb()

    table = dynamodb.Table('rulesTable')
    response = table.put_item(
        Item={
            'RuleId': 1
        }
    )
    return response


def list_tables() -> List[str]:
    dynamodb = get_dynamodb()
    table_iterator = dynamodb.tables.one()
    return [table.name for table in table_iterator]


def load_rules(rules: dict, table_name: str = "rulesTable") -> None:
    dynamodb = get_dynamodb()
    table = dynamodb.Table(table_name)
    for rule in rules:
        table.put_item(Item=rule)


def delete_table(table_name: str) -> None:
    dynamodb = get_dynamodb()
    table = dynamodb.Table(table_name)
    table.delete()
