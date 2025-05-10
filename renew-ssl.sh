#!/bin/bash
# Script para renovar certificados SSL do Let's Encrypt

echo "=== Iniciando renovação de certificados SSL ==="
echo "Parando os contêineres Docker..."
docker-compose down

echo "Renovando certificados..."
sudo certbot renew

echo "Reiniciando os contêineres Docker..."
docker-compose up -d

echo "=== Renovação concluída! ==="
echo "Você pode verificar a validade dos certificados com:"
echo "sudo certbot certificates"