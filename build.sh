#!/usr/bin/env bash
# exit on error
set -o errexit

pip install pytz
poetry install
pip install stripe --no-binary :all:

python manage.py collectstatic --no-input

