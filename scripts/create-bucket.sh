#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket data-transform-local-deploy --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket xml-data --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket json-data --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3 cp src/data s3://xml-data --recursive
aws --endpoint-url=$AWS_ENDPOINT s3api put-bucket-notification-configuration --bucket xml-data --notification-configuration '{"LambdaFunctionConfigurations":[{"Events":["s3:ObjectCreated:*"],"LambdaFunctionArn":"arn:aws:lambda:eu-central-1:000000000000:function:data-transform-local-processing"}]}'
