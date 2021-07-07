import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../package')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import json
import logging
import s3_api as s3
import dynamodb_api as D
import converter as converter

S3_ERROR_RESPONSE = {"body": json.dumps({"message": "S3 error"}), "statusCode": 500}
DYNAMO_ERROR_RESPONSE = {"body": json.dumps({"message": "DynamoDB error"}), "statusCode": 500}
NO_EVENT_ERROR = {"body": json.dumps({"message": "Missing mandatory parameter: EVENT"}), "statusCode": 400}


def process(event: dict = None, context: object = None) -> dict:
    if not event:
        return NO_EVENT_ERROR
    dynamodb_table = event.get("dynamodb_resource", "rulesTable")
    to_bucket = event.get("to_bucket", "json-data")
    rules = D.get_rules(table=dynamodb_table)
    if not rules:
        return DYNAMO_ERROR_RESPONSE
    events = []
    for record in event["Records"]:
        events.append(f'{record["eventName"]} {record["s3"]["object"]["key"]}')
        try:
            process_event(record, to_bucket, rules)
        except IOError as e:
            return S3_ERROR_RESPONSE

    return {
        "body": json.dumps({"message": f"SUCCESS! Events: {', '.join(events)} were processed"}),
        "statusCode": 200
    }


def process_event(event: dict, to_bucket: str, rules: dict) -> None:
    """
    Process recieved event, retrieve metadata, download xml, convert xml file to json and upload to s3
    No core logic here, s3api and converter modules are unit tested
    """
    event_name = event["eventName"]
    from_bucket = event["s3"]["bucket"]["name"]
    file_prefix = event["s3"]["object"]["key"].split(".xml")[0]

    logging.info(f"Received an event: Name: {event_name}, Bucket: {from_bucket}, File: {file_prefix}")
    xml_string = s3.get_object_as_string(from_bucket, f"{file_prefix}.xml")
    if not xml_string:
        raise IOError
    json_string = converter.xml_to_json(xml_string, rules)
    success = s3.put_object(to_bucket, f"{file_prefix}.json", json_string)
    if not success:
        raise IOError

    logging.info(f"Save ** {file_prefix}.json ** to {to_bucket} S3 bucket")
