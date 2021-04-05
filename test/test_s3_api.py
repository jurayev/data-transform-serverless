import os
import sys

# resolves import conflicts between modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../app/src')))
import logging
import pytest
import s3_api as s3


@pytest.fixture
def prepare_bucket(bucket):
    """
    Anything before yield executed before the test
    Anything after yield executed after the test
    """
    logging.info("Create bucket")
    s3.create_bucket(bucket)
    yield
    logging.info("Delete bucket")
    s3.delete_bucket(bucket)


@pytest.mark.parametrize('bucket', ["test-bucket"])
def test_create_bucket(prepare_bucket, bucket: str):
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
def test_delete_object(prepare_bucket, bucket: str):
    obj = "test-obj.txt"
    s3.put_object(bucket, obj, "test body")
    s3.delete_object(bucket, obj)
    objects = [some_object['Key'] for some_object in s3.list_objects(bucket)]
    assert obj not in objects


@pytest.mark.parametrize('bucket', ["test-bucket-put-object"])
def test_put_object(prepare_bucket, bucket: str):
    obj = "test-put-obj.txt"
    s3.put_object(bucket, obj, "test body")
    objects = [some_object['Key'] for some_object in s3.list_objects(bucket)]
    assert obj in objects


@pytest.mark.parametrize('bucket', ["test-bucket-get-object"])
def test_get_object(prepare_bucket, bucket: str):
    obj = "test-obj.txt"
    test_content = "test body"
    s3.put_object(bucket, obj, test_content)
    string_obj = s3.get_object_as_string(bucket, obj)
    assert test_content == string_obj


@pytest.mark.parametrize('bucket', ["test-bucket-upload-object"])
def test_presigned_post(prepare_bucket, bucket: str):
    obj = "uploads/test-obj.txt"
    response = s3.create_presigned_post(bucket_name=bucket, object_name=obj)
    assert bucket == response['url'].split("/")[-1]
    assert obj == response['fields']["key"]
