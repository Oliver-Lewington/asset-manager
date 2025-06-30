#!/usr/bin/env bash
# Exit on error
set -o errexit

python -m gunicorn asset_manager.asgi:application -k uvicorn.workers.UvicornWorker