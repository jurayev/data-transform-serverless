#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

pip install pytest
pip install requests
python3 -m pytest
