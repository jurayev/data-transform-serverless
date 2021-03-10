import os
import sys
# resolves import conflicts between modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
import json
from file_processing import handler
import s3_api as s3


@pytest.fixture
def setup_and_teardown(xml_bucket, json_bucket):
    """
    Anything before yield executed before the test
    Anything after yield executed after the test
    """
    print("\nsetting up: create bucket and put a new object")
    s3.create_bucket(xml_bucket)
    s3.create_bucket(json_bucket)
    with open("test/mock_data/data.xml", 'rb') as f:
        data = f.read().decode('utf-8')
    s3.put_object(xml_bucket, "data.xml", data)
    yield
    print("\ntearing down: delete bucket")
    s3.delete_bucket(xml_bucket)
    s3.delete_bucket(json_bucket)

@pytest.mark.parametrize('xml_bucket, json_bucket', [("test-xml-bucket", "test-json-bucket")])
def test_xml_json_tranform(setup_and_teardown, xml_bucket, json_bucket):
    with open("test/events/s3-put-event.json", 'r') as f:
        event = json.loads(f.read())
    
    response = handler(event=event, to_bucket=json_bucket)
    expected_object = "data.json"
    actual_object = ""
    objects = s3.list_objects(json_bucket)
    for obj in objects:
        if obj["Key"] == expected_object:
            actual_object = expected_object
    assert 200 == response["status"]
    assert expected_object == actual_object

def test_xml_json_tranform_returns_error():
    with open("test/events/s3-put-event.json", 'r') as f:
        event = json.loads(f.read())
    
    response = handler(event=event)
    
    assert 500 == response["status"]
