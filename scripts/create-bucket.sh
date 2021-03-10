#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket data-transform-local-deploy --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket xml-data --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3api create-bucket --bucket json-data --region eu-central-1
aws --endpoint-url=$AWS_ENDPOINT s3 cp src/data s3://xml-data --recursive