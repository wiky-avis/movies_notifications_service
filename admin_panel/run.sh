#!/usr/bin/env bash

set -e

# Start server
echo "Starting server"
gunicorn --worker-class=uvicorn.workers.UvicornWorker --workers=1 -b ${NAP_APP__HOST}:${NAP_APP__PORT} app:app
