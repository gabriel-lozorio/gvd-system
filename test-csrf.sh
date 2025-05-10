#!/bin/bash
# Script para testar a configuração de CSRF do sistema

DOMAIN=${1:-"gvd-system.com.br"}
HTTP_URL="http://${DOMAIN}"
HTTPS_URL="https://${DOMAIN}"

echo "=== Testando configuração de CSRF para ${DOMAIN} ==="
echo ""

# Testar conexão HTTP básica
echo "1. Testando conexão HTTP básica..."
curl -s -I ${HTTP_URL} | grep -E 'HTTP|Location|CSRF|Set-Cookie'
echo ""

# Testar redirecionamento HTTP para HTTPS
echo "2. Testando redirecionamento HTTP → HTTPS..."
curl -s -I -L ${HTTP_URL} | grep -E 'HTTP|Location|CSRF|Set-Cookie'
echo ""

# Testar cabeçalhos HTTPS
echo "3. Verificando cabeçalhos HTTPS..."
curl -s -I ${HTTPS_URL} | grep -E 'HTTP|Strict|CSRF|X-|Set-Cookie'
echo ""

# Testar obtenção de token CSRF
echo "4. Tentando obter token CSRF via requisição GET..."
CSRF_COOKIE=$(curl -s -c - ${HTTPS_URL} | grep csrf)
echo "${CSRF_COOKIE}"
echo ""

# Testar uma operação POST com CSRF
if [ -n "${CSRF_COOKIE}" ]; then
  CSRF_TOKEN=$(echo "${CSRF_COOKIE}" | awk '{print $7}')
  echo "5. Testando POST com token CSRF ${CSRF_TOKEN}..."
  echo "   (Esta solicitação deve falhar, pois o token está sendo usado incorretamente)"
  curl -s -X POST \
    -b "csrftoken=${CSRF_TOKEN}" \
    -H "X-CSRFToken: ${CSRF_TOKEN}" \
    -H "Origin: ${HTTPS_URL}" \
    -H "Referer: ${HTTPS_URL}/login/" \
    -d "username=test&password=test" \
    "${HTTPS_URL}/users/login/" -i | grep -E 'HTTP|CSRF|Location'
  echo ""
fi

echo "=== Testes concluídos ==="
echo ""
echo "Dicas para solução de problemas de CSRF:"
echo "1. Verifique se o cookie CSRF está sendo definido corretamente"
echo "2. Confirme que o domínio CSRF corresponde ao domínio da solicitação"
echo "3. Verifique se o cabeçalho Origin está na lista CSRF_TRUSTED_ORIGINS"
echo "4. Examine os logs em /app/logs/django-csrf.log para mensagens detalhadas"