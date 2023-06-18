#!/usr/bin/env bash

set -e

# Start server
echo "Starting server"
gunicorn --worker-class=uvicorn.workers.UvicornWorker --workers=1 -b ${TEMPLATE_APP__HOST}:${TEMPLATE_APP__PORT} admin_panel.app:app
