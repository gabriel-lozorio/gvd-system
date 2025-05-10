#!/bin/bash
# Script para monitoramento do sistema GVD
echo "=== Monitoramento do Sistema GVD ==="
echo "Data: $(date)"
echo

# Verificar status dos contêineres
echo "=== Status dos Contêineres ==="
docker-compose ps
echo

# Verificar logs recentes do serviço web
echo "=== Logs Recentes do Serviço Web ==="
docker-compose logs --tail=20 web
echo

# Verificar espaço em disco
echo "=== Espaço em Disco ==="
df -h
echo