#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

chmod +x scripts/set-vars.sh
. scripts/set-vars.sh
cd src
serverless deploy --verbose --stage local --force
# serverless deploy --stage production
cd ..