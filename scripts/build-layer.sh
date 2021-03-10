#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

rm -rf src/package
cd src
pip install --target ./package -r requirements.txt
cd ..