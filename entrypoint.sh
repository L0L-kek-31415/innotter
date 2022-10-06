#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $DJANGO_DB_HOST $DJANGO_DB_PORT; do
  sleep 0.1
done

echo "PostgreSQL started"

python3 manage.py migrate
python3 manage.py runserver  0.0.0.0:8000

exec "$@"