#!/bin/sh

echo "Waiting for web..."

while ! nc -z "localhost" "8000"; do
  sleep 0.1
done

echo "web started"

celery -A core worker -l info

exec "$@"