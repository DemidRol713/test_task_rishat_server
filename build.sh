#!/usr/bin/env bash
# exit on error
set -o errexit
pip install pytz
poetry install

python manage.py collectstatic --no-input

