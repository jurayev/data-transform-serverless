#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

# Set env vars
chmod +x scripts/set-vars.sh
. scripts/set-vars.sh
# Install deps
chmod +x scripts/build-layer.sh
. scripts/build-layer.sh
# Prep buckets and data
aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket data-transform-local-deploy --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket xml-data --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket json-data --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3api put-bucket-notification-configuration --bucket xml-data --notification-configuration '{"LambdaFunctionConfigurations":[{"Events":["s3:ObjectCreated:*"],"LambdaFunctionArn":"arn:aws:lambda:eu-central-1:000000000000:function:data-transform-local-processing"}]}'
# Run Tests
chmod +x scripts/tests.sh
. scripts/tests.sh
# Put objects to bucket that triggers lambda
aws --endpoint-url=$AWS_ENDPOINT s3 cp src/data s3://xml-data --recursive
while true; do
  echo "Running Docker"
  sleep 2
done

echo "DONE"