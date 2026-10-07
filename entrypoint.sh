#!/bin/sh
set -e

echo "Waiting for PostgreSQL to be ready..."
while ! nc -z db 5432; do
  sleep 1
done
echo "PostgreSQL is up."

echo "Running Alembic migrations..."
alembic upgrade head

echo "Seeding database (if empty)..."
python seed.py || echo "Seed skipped."

echo "Starting Gunicorn..."
exec gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 60 "app.main:create_app()"