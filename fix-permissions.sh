#!/bin/sh
set -e

echo "Corrigindo permissões dos arquivos estáticos..."
docker-compose exec -u 0 web mkdir -p /app/staticfiles /app/media
docker-compose exec -u 0 web chmod -R 777 /app/staticfiles /app/media
docker-compose exec -u 0 web python manage.py collectstatic --noinput

echo "Permissões corrigidas com sucesso!"