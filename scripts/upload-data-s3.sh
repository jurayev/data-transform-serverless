#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

aws --endpoint-url=$AWS_ENDPOINT s3 cp app/data s3://xml-data --recursive
