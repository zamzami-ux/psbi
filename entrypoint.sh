#!/bin/sh
set -e

# Wait for DB if using postgres (simple loop)
if [ -n "$DATABASE_URL" ]; then
  echo "DATABASE_URL is set, continuing..."
fi

echo "Apply database migrations..."
python manage.py migrate --noinput

echo "Collect static files..."
python manage.py collectstatic --noinput

exec "$@"
