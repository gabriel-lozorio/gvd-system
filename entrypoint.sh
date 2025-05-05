#!/bin/sh
# entrypoint.sh: Container initialization script
#
# This script ensures that all required services are available before starting
# the application. It will:
# 1. Wait for PostgreSQL database to be ready
# 2. Wait for Redis to be ready
# 3. Apply database migrations
# 4. Collect static files
# 5. Start the application (command passed to the container)

# Configure default connection parameters for PostgreSQL
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

echo "Trying to connect to PostgreSQL at $DB_HOST:$DB_PORT..."
# Use ping para verificar se o host é acessível
until ping -c 1 $DB_HOST >/dev/null 2>&1; do
  echo "PostgreSQL host not reachable, waiting..."
  sleep 2
done

# Agora use nc para verificar a porta específica
until nc -z $DB_HOST $DB_PORT; do
  echo "PostgreSQL port not available, waiting..."
  sleep 0.5
done
echo "PostgreSQL started"

# Wait for Redis
echo "Waiting for Redis..."
until nc -z redis 6379; do
  echo "Redis not available, waiting..."
  sleep 0.5
done
echo "Redis started"

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting service..."
exec "$@"