#!/usr/bin/env bash
# Exit on error
set -o errexit

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# python -m gunicorn asset_manager.asgi:application -k uvicorn.workers.UvicornWorker
python manage.py runserver