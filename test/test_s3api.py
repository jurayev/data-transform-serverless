import os
import sys
# resolves import conflicts between modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import pytest
import json
from file_processing import handler
import s3_api as s3

@pytest.fixture
def prepare_bucket(bucket):
    """
    Anything before yield executed before the test
    Anything after yield executed after the test
    """
    print("\ncreate bucket")
    s3.create_bucket(bucket)
    yield
    print("\ndelete bucket")
    s3.delete_bucket(bucket)

@pytest.mark.parametrize('bucket', ["test-bucket"])
def _test_create_bucket(prepare_bucket, bucket):
    s3.create_bucket(bucket)
    assert bucket in s3.list_buckets()

def test_delete_bucket():
    bucket = "test-del-bucket"
    s3.create_bucket(bucket)
    s3.delete_bucket(bucket)
    assert bucket not in s3.list_buckets()

def test_list_buckets():
    assert type(s3.list_buckets()) == list

def test_list_objects():
    assert type(s3.list_objects("xml")) == list

@pytest.mark.parametrize('bucket', ["test-bucket-object"])
def test_delete_object(prepare_bucket, bucket):
    obj = "test-obj.txt"
    s3.put_object(bucket, obj, "test body")
    s3.delete_object(bucket, obj)
    objects = [some_object['Key'] for some_object in s3.list_objects(bucket)]
    assert obj not in objects

@pytest.mark.parametrize('bucket', ["test-bucket-put-object"])
def test_put_object(prepare_bucket, bucket):
    obj = "test-put-obj.txt"
    s3.put_object(bucket, obj, "test body")
    objects = [some_object['Key'] for some_object in s3.list_objects(bucket)]
    assert obj in objects

@pytest.mark.parametrize('bucket', ["test-bucket-get-object"])
def test_get_object(prepare_bucket, bucket):
    obj = "test-obj.txt"
    test_content = "test body"
    s3.put_object(bucket, obj, test_content)
    string_obj = s3.get_object_as_string(bucket, obj)
    assert test_content == string_obj
