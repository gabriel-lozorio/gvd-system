#!/bin/bash
# check_connectivity.sh

echo "=== Teste de Conectividade do Sistema Financeiro GVD ==="
echo "Testando a rede Docker..."
docker network ls | grep sistema

echo "Verificando containers em execução..."
docker-compose ps

echo "Testando conexão do web para o banco de dados..."
docker-compose exec web ping -c 2 db

echo "Testando conexão do web para o Redis..."
docker-compose exec web ping -c 2 redis

echo "Testando conexão do banco de dados..."
docker-compose exec db pg_isready -U financeiro

echo "Verificando logs do container web..."
docker-compose logs --tail=20 web

echo "=== Verificação concluída ==="