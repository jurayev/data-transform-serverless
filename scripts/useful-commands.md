# Serverless - Commands and references
npm install -g serverless
npm install serverless-localstack --dev
serverless deploy --verbose --stage local

## invoke lambda function
serverless invoke --function process --log --stage local --region eu-central-1 --path events/s3-put-event.json
serverless invoke --function process --log --stage local --payload fileb://lambda_upload_input.json response.json
serverless invoke --function process --stage local --region eu-central-1 --path events/s3-event.json --type Event 
## logs
serverless logs --stage local --tail -i 10 -f processing


## deployment bucket
awslocal s3api create-bucket --bucket transform-local-deploy --region eu-central-1

## list files s3:  
awslocal s3 ls s3://xml --recursive
## copy files s3:  
awslocal s3 cp ./test/files s3://xml//xml-files/ --recursive
## create new folder: 
awslocal s3api put-object --bucket xml --key xml-files
## create bucket:  
awslocal s3 mb s3://xml
## list buckets: 
awslocal s3api list-buckets
## list objects:
awslocal s3api list-objects --bucket profile-pictures
## delete bucket
awslocal s3api delete-bucket --bucket name
## s3 config notification
aws --endpoint-url=$AWS_ENDPOINT s3api put-bucket-notification-configuration --bucket xml-data --notification-configuration '{"LambdaFunctionConfigurations":[{"Events":["s3:ObjectCreated:*"],"LambdaFunctionArn":"arn:aws:lambda:eu-central-1:000000000000:function:data-transform-local-processing"}]}'


# Docker
docker-compose up
docker run --env LOCALSTACK_HOSTNAME=172.17.0.3 -p 9000:8080 384e69706200
docker build -t serverless-test -f Dockerfile.build . 
docker network inspect build 
docker network connect multi-host-network <container_id>
docker-compose up -d --no-deps --build <service_name>
docker exec -it <container_id> /bin/sh
docker run --rm --env LOCALSTACK_HOSTNAME=172.17.0.2 -p 9001:8080 466dbb6b1517<container_id>

# DynamoDB:
## data types
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DynamoDBMapper.DataTypes.html
https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_AttributeValue.html
https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GettingStarted.Python.05.html

awslocal dynamodb create-table --table-name Rules --attribute-definitions AttributeName=RuleId,AttributeType=N --key-schema AttributeName=RuleId,KeyType=HASH --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5
awslocal dynamodb delete-table --table-name Rules

## check table
awslocal dynamodb describe-table --table-name rulesTable
awslocal dynamodb list-tables
awslocal dynamodb get-item --consistent-read --table-name rulesTable --key '{"RuleId": {"N": "1"}}'




# API GATEWAY
https://www.serverless.com/framework/docs/providers/aws/events/apigateway/#simple-http-endpoint
https://stackoverflow.com/questions/50925083/parse-multipart-request-string-in-python
## list all api endpoints
awslocal apigateway get-rest-apis
## list all endpoints
awslocal apigateway get-resources --rest-api-id 575os36mtj
## hit endpoint
curl -X POST -H "Content-Type: application/xml" --data-binary "@src/data/test.xml" http://localhost:4566/restapis/<api id>/local/_user_request_/upload?file=test.xml --data '{"file": "test.xml"}'
curl -X POST "http://localhost:4566/restapis/ooqtshw5rg/local/_user_request_/upload?file=data/data.xml&bucket=xml-data"
curl -F "name=data.xml" -F "file=@src/data/data.xml" http://localhost:4566/restapis/ku4nexn8h4/local/_user_request_/upload

## upload file using presigned url
curl -F "acl=public-read" \
      -F "file=@src/test/test.xml" \
      -F "Content-Type=application/xml" \
      -F "key=uploads/test.xml" \
      -F "x-amz-algorithm=AWS4-HMAC-SHA256" \
      -F "x-amz-credential=test/20210402/eu-central-1/s3/aws4_request" \
      -F "x-amz-date=20210402T220531Z" \
      -F "x-amz-signature=fba9f35caee211f24bcb7c9cfb03ff670de9e10f271ae3e58422746195578e6c" \
      http://localhost:4566/xml-data

# Lambda layers
https://medium.com/@dorian599/serverless-aws-lambda-layers-and-python-dependencies-92741138bf31
https://github.com/dorian599/serverless-medium