import json
import logging
import s3_api as s3
import converter as converter
import rules as mock_rules
from botocore.exceptions import ClientError

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
ERROR_RESPONSE = {"message": "S3 error", "status": 500}

def handler(event=None, context=None, to_bucket="json-data"):
    """
    Process recieved event, retrieve metadata, download xml, convert xml file to json and upload to s3
    No core logic here, s3api and converter modules are unit tested
    """
    event_name = event["Records"][0]["eventName"]
    from_bucket = event["Records"][0]["s3"]["bucket"]["name"]
    file_prefix = event["Records"][0]["s3"]["object"]["key"].split(".xml")[0]
 
    LOGGER.info(f"Recieved an event: {event_name}")
    xml_string = s3.get_object_as_string(from_bucket, f"{file_prefix}.xml")
    # I assume the xml always valid, else validate_xml(xml_string) function is needed
    if not xml_string: 
        return ERROR_RESPONSE
    # I assume that rules are stored in NoSQL DB or S3 as json and fetched by rule id or file id
    # rules = db.get(rule_id)
    rules = mock_rules.RULES
    json_string = converter.xml_to_json(xml_string, rules)
    success = s3.put_object(to_bucket, f"{file_prefix}.json", json_string)
    if not success:
        return ERROR_RESPONSE
    
    LOGGER.info(f"Save ** {file_prefix}.json ** to {to_bucket} S3 bucket")
    return {
        "message": f" SUCCESS! ** {file_prefix}.xml ** has been converted to ** {file_prefix}.json **",
        "status": 200
    }