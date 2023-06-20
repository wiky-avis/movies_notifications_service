#!/usr/bin/env bash

set -e

# Start server
echo "Starting server"
gunicorn --worker-class=uvicorn.workers.UvicornWorker --workers=4 -b ${NA_APP_HOST}:${NA_APP_PORT} src.app:app
