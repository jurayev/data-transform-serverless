#!/bin/bash
set -o errexit
set -o pipefail
set -o nounset

rm -rf `find . -name '*.pytest_cache'`
rm -rf `find . -name __pycache__`
rm -rf `find . -name '*.egg-info'`
rm -rf `find . -name '*.DS_Store'`
rm -rf `find . -name '*.idea'`
rm -rf `find . -name '*.serverless'`
find . -type f -name '*.py[co]'  -delete
find . -type f -name '*~'  -delete
find . -type f -name '.*~'  -delete
find . -type f -name '@*'  -delete
find . -type f -name '#*#'  -delete
find . -type f -name '*.orig'  -delete
find . -type f -name '*.rej'  -delete
rm -f .coverage
rm -rf coverage
rm -rf build
rm -rf htmlcov
rm -rf dist
rm -rf .pytest_cache
