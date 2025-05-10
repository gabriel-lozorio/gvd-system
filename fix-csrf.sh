#!/bin/bash
# Script para reiniciar o sistema e verificar a configuração CSRF

echo "Parando os contêineres..."
docker-compose down

echo "Reconstruindo o contêiner web..."
docker-compose build web

echo "Iniciando os contêineres..."
docker-compose up -d

echo "Aguardando 10 segundos para inicialização..."
sleep 10

echo "Verificando logs para erros..."
docker-compose logs web | grep -i error

echo "Verificando configuração CSRF..."
echo "Hosts confiáveis:"
docker-compose exec web python -c "from django.conf import settings; print(settings.CSRF_TRUSTED_ORIGINS)"

echo "Verificando se o sistema está online..."
curl -s -I https://gvd-system.com.br | grep -E "HTTP|CSRF"

echo "Para verificar se o CSRF está funcionando corretamente, tente fazer login no sistema."
echo "Se encontrar erros de CSRF, execute: docker-compose logs web | grep -i csrf"