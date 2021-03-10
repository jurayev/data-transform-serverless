#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

export AWS_ACCESS_KEY_ID=test
export AWS_SECRET_ACCESS_KEY=test
export AWS_ENDPOINT=http://$LOCALSTACK_HOSTNAME:4566
export AWS_REGION=eu-central-1
export AWS_ENV=test