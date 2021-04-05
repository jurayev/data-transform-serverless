#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

chmod +x scripts/set-vars.sh
. scripts/set-vars.sh
cd app
serverless invoke --function process --log --stage local --region eu-central-1 --path events/s3-put-event.json
cd ..
