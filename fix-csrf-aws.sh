#!/bin/bash
# Script simplificado para resolver problemas de CSRF no AWS Lightsail

echo "=== Iniciando correção de CSRF no AWS Lightsail ==="

# Parar contêineres
echo "Parando contêineres..."
docker-compose down

# Limpar arquivos de log que podem causar problemas
echo "Limpando arquivos de log..."
mkdir -p logs
touch logs/django-csrf.log
chmod 666 logs/django-csrf.log

# Reconstruir o contêiner web
echo "Reconstruindo contêiner web..."
docker-compose build web

# Iniciar sistema
echo "Iniciando sistema..."
docker-compose up -d

# Aguardar inicialização
echo "Aguardando inicialização..."
sleep 15

# Verificar logs
echo "Verificando logs..."
docker-compose logs --tail=30 web

echo ""
echo "=== Correção concluída ==="
echo "Para verificar se o CSRF está funcionando:"
echo "1. Acesse https://gvd-system.com.br/core/csrf-test/"
echo "2. Verifique se consegue submeter o formulário"
echo ""
echo "Se ainda tiver problemas, consulte o arquivo CSRF-DEBUG.md"