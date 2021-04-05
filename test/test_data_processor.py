import os
import sys

# resolves import conflicts between modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/src')))
import pytest
import json
import s3_api as s3
import dynamodb_api as db
import logging
from data_processor import process


@pytest.fixture
def setup_and_teardown(xml_bucket: str, json_bucket: str):
    """
    Anything before yield executed before the test
    Anything after yield executed after the test
    """
    logging.info("Setting up: create s3 and dynamodb resources")
    s3.create_bucket(xml_bucket)
    s3.create_bucket(json_bucket)
    with open("test/mock_data/data.xml", 'rb') as f:
        data = f.read().decode('utf-8')
    s3.put_object(xml_bucket, "data.xml", data)
    # dynamo create table
    db.create_rules_table("TestProcessingRules")
    # dynamo load data
    with open("test/mock_data/rules.json", 'rb') as f:
        fake_rules = json.load(f)
    db.load_rules(fake_rules, "TestProcessingRules")
    yield
    logging.info("Tearing down: delete s3 and dynamodb resources")
    s3.delete_bucket(xml_bucket)
    s3.delete_bucket(json_bucket)
    # dynamo remove table
    db.delete_table("TestProcessingRules")


@pytest.mark.parametrize('xml_bucket, json_bucket', [("test-xml-bucket", "test-json-bucket")])
def test_xml_json_transform(setup_and_teardown, xml_bucket: str, json_bucket: str):
    with open("test/events/s3-put-event.json", 'r') as f:
        event = json.loads(f.read())
    event["to_bucket"] = json_bucket
    event["dynamodb_resource"] = "TestProcessingRules"
    response = process(event=event)
    expected_object = "data.json"
    actual_object = ""
    objects = s3.list_objects(json_bucket)
    for obj in objects:
        if obj["Key"] == expected_object:
            actual_object = expected_object
    assert 200 == response["statusCode"]
    assert expected_object == actual_object


def test_xml_json_transform_returns_error():
    with open("test/events/s3-put-event.json", 'r') as f:
        event = json.loads(f.read())
    response = process(event=event)
    assert 500 == response["statusCode"]
