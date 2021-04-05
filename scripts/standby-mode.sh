#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

echo "INFO: 1. Setting env vars"
chmod +x scripts/set-vars.sh
. scripts/set-vars.sh

echo "INFO: 2. Installing deps"
chmod +x scripts/build-layer.sh
. scripts/build-layer.sh

echo "INFO: 3. Prepopulating data"
chmod +x scripts/prepare-data-dynamodb.sh
. scripts/prepare-data-dynamodb.sh

echo "INFO: 4. Running Tests"
chmod +x scripts/tests.sh
. scripts/tests.sh

echo "INFO: 5. Deploy serverless"
chmod +x scripts/deploy.sh
. scripts/deploy.sh

echo "INFO: 6. Runing container in standby mode until terminated"
while true; do
  echo "Running Docker"
  sleep 5
done

echo "INFO: TERMINATED"
