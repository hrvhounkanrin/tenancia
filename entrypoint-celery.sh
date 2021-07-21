#!/bin/sh
mkdir -p "LOGS"
# celery -b rabbitmq -A meslimmo.celery worker --loglevel=debug
# Start server
echo "Starting server"
exec "$@"
