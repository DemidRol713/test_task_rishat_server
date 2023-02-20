#!/usr/bin/env bash
# exit on error
set -o errexit


pip install pytz
poetry install
/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
/opt/render/project/src/.venv/bin/python -m pip install stripe
#python -m pip install requests
python manage.py collectstatic --no-input

