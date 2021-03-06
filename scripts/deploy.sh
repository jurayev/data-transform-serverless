#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

chmod +x scripts/set-vars.sh
. scripts/set-vars.sh
cd app
# Local env
serverless deploy --verbose --stage local --force

# Prod env
# serverless deploy --stage production
cd ..
