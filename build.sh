#!/usr/bin/env bash
# exit on error
set -o errexit
/opt/render/project/src/.venv/bin/python -m pip install --upgrade pip
pip3 install -r requirements.txt
poetry install

python manage.py collectstatic --no-input

