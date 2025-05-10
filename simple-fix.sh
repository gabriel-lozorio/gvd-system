#!/bin/bash
# Script ultra-simplificado para corrigir CSRF no AWS Lightsail

# Parar containers
docker-compose down

# Verificar script
if [ -x "$(command -v dos2unix)" ]; then
  dos2unix *.sh
  dos2unix config/lightsail_settings.py
else
  echo "dos2unix não está instalado. Ignorando conversão de arquivos."
fi

# Criar diretórios necessários
mkdir -p logs
chmod 777 logs

# Recriar containers
docker-compose up -d

echo "Containers reiniciados. Verifique se o problema CSRF foi resolvido."
echo "Acesse: https://gvd-system.com.br/core/csrf-test/"