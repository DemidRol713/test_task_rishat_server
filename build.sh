#!/usr/bin/env bash
# exit on error
set -o errexit
pip3 install -r requirements.txt
poetry install

python manage.py collectstatic --no-input

