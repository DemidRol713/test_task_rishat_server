#!/usr/bin/env bash
# exit on error
set -o errexit

pip install pytz
poetry install
python stripe-python-5.2.0/setup.py install


python manage.py collectstatic --no-input

