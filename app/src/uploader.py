import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../package')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
import json
import logging
import requests
import s3_api as s3
import datetime

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
S3_ERROR_RESPONSE = {"body": json.dumps({"message": "S3 file upload error"}), "statusCode": 500}
NO_EVENT_ERROR = {"body": json.dumps({"message": "Missing mandatory parameter: EVENT"}), "statusCode": 400}


def upload(event: dict = None, context: object = None) -> dict:
    """
    Uploads file as multipart/data-form to S3 bucket.
    First generates presigned url for post request
    Then uploads file by specified file name (currently implemented as work around,
    otherwise user can use presigned url to access S3 bucket)
    """
    if not event:
        return NO_EVENT_ERROR

    LOGGER.info("Received upload event!")
    LOGGER.info(json.dumps(event, indent=4))

    file_name = event["queryStringParameters"]['file']
    bucket_name = event["queryStringParameters"]['bucket']
    s3_response = s3.create_presigned_post(bucket_name=bucket_name, object_name="uploads/" + file_name)
    if not s3_response:
        return S3_ERROR_RESPONSE

    data = s3_response['fields']
    url = s3_response['url']

    # Read file from local disk as a workaround solution
    with open(file_name, 'rb') as f:
        files = {'file': f}
        http_response = requests.post(url, data=data, files=files)

    # If successful, returns HTTP status code 204
    logging.info(f'File upload HTTP status code: {http_response.status_code}')
    if http_response.status_code != 204:
        return S3_ERROR_RESPONSE
    body = {
        "message": f"SUCCESS! File {file_name} was uploaded",
        "createdAt": str(datetime.datetime.now().time()),
        "data": data,
        "url": url
    }
    response = {
        "statusCode": http_response.status_code,
        "body": json.dumps(body)
    }
    return response
