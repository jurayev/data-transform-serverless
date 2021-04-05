#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

rm -rf app/package
pip install --target app/package -r app/requirements.txt
