import os
import sys

# resolves import conflicts between modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/src')))
import pytest
import json
import uploader
import s3_api as s3
import logging


@pytest.fixture
def setup_and_teardown(bucket: str):
    """
    Anything before yield executed before the test
    Anything after yield executed after the test
    """
    logging.info("Create bucket")
    s3.create_bucket(bucket)
    yield
    logging.info("Delete bucket")
    s3.delete_bucket(bucket)


@pytest.mark.parametrize("bucket", ["test-xml-bucket"])
def test_upload(setup_and_teardown, bucket: str):
    obj = "test/mock_data/data.xml"
    event = {"queryStringParameters": {"file": obj, "bucket": bucket}}
    response = uploader.upload(event, {})
    url = json.loads(response["body"])["url"]
    assert 204 == response["statusCode"]
    assert bucket == url.split("/")[-1]
    assert s3.get_object_as_string(bucket, "uploads/" + obj) != ""


def test_upload_s3_error():
    obj = "test/mock_data/data.xml"
    bucket = "invalid-xml-bucket"
    event = {"queryStringParameters": {"file": obj, "bucket": bucket}}
    response = uploader.upload(event, {})
    message = json.loads(response["body"])["message"]
    assert 500 == response["statusCode"]
    assert message == "S3 file upload error"
