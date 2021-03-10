#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset
# Set env vars
chmod +x scripts/set-vars.sh
. scripts/set-vars.sh
# Build dependecies
chmod +x scripts/build-layer.sh
. scripts/build-layer.sh
# Prep buckets and data
chmod +x scripts/create-bucket.sh
. scripts/create-bucket.sh
# Run Tests
chmod +x scripts/tests.sh
. scripts/tests.sh
#Deploy serverless
chmod +x scripts/deploy.sh
. scripts/deploy.sh
# Invoke lambda
chmod +x scripts/invoke.sh
. scripts/invoke.sh
# Clean up resources
chmod +x scripts/cleanup.sh
. scripts/cleanup.sh
