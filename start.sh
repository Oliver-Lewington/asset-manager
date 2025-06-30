#!/usr/bin/env bash
# Exit on error
set -o errexit

python -m venv venv
source venv/bin/activate

python -m gunicorn asset_manager.asgi:application -k uvicorn.workers.UvicornWorker