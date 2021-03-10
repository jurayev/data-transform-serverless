#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

pip install pytest
python3 -m pytest