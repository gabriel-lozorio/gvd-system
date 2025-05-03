#!/bin/bash
# entrypoint.sh

# Esperar pelo banco de dados
echo "Esperando pelo PostgreSQL..."
while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  sleep 0.1
done
echo "PostgreSQL iniciado"

# Aplicar migrações
python manage.py migrate --noinput

# Coletar arquivos estáticos
python manage.py collectstatic --noinput

# Iniciar Gunicorn
exec "$@"