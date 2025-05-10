#!/bin/sh
# entrypoint.sh: Container initialization script
#
# This script ensures that all required services are available before starting
# the application.

# Configure default connection parameters
DB_HOST=${DB_HOST:-db}
DB_PORT=${DB_PORT:-5432}

# Ensure directory permissions
ensure_permissions() {
  echo "Checking directory permissions..."
  if [ ! -w "/app/staticfiles" ] || [ ! -w "/app/media" ]; then
    echo "Warning: Permission issues detected with staticfiles or media directories"
    # We'll continue anyway since USER directive should have fixed this
  fi
}

# Wait for PostgreSQL
echo "Trying to connect to PostgreSQL at $DB_HOST:$DB_PORT..."
until ping -c 1 $DB_HOST >/dev/null 2>&1; do
  echo "PostgreSQL host not reachable, waiting..."
  sleep 2
done

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

# Verify permissions
ensure_permissions

# Limpeza de logs (simplificar configuração)
echo "Simplificando configuração de logging..."

# Print current settings module for diagnostic
echo "Current Django settings module: $DJANGO_SETTINGS_MODULE"
python -c "import os, sys; print(f'Python path: {sys.path}')"
python -c "import os; from django.conf import settings; print(f'Debug mode: {settings.DEBUG}'); print(f'CSRF trusted origins: {settings.CSRF_TRUSTED_ORIGINS}')" || echo "Could not load Django settings"

# Apply database migrations (with error handling)
echo "Applying database migrations..."
python manage.py migrate --noinput || {
  echo "Migration error detected. Attempting to continue..."
  # We'll continue even if migrations fail for now
}

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput --clear || {
  echo "Warning: Static file collection issue detected"
  echo "Trying with more verbose output..."
  python manage.py collectstatic --noinput -v 2 || {
    echo "Static file collection failed. Some files may be missing."
  }
}

# Verificar configurações CSRF
echo "Verificando configurações CSRF..."
python -c "from django.conf import settings; print(f'CSRF trusted origins: {settings.CSRF_TRUSTED_ORIGINS}')" || echo "Não foi possível verificar configurações CSRF"

# Diagnosticar configuração atual
echo "Configuração atual do sistema:"
echo "DEBUG: $(python -c "from django.conf import settings; print(settings.DEBUG)")"
echo "ALLOWED_HOSTS: $(python -c "from django.conf import settings; print(settings.ALLOWED_HOSTS)")"
echo "CSRF_COOKIE_SECURE: $(python -c "from django.conf import settings; print(settings.CSRF_COOKIE_SECURE)")"
echo "CSRF_COOKIE_DOMAIN: $(python -c "from django.conf import settings; print(settings.CSRF_COOKIE_DOMAIN)")"
echo "SECURE_PROXY_SSL_HEADER: $(python -c "from django.conf import settings; print(settings.SECURE_PROXY_SSL_HEADER)")"

# Start the service
echo "Starting service..."
exec "$@"