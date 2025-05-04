#!/bin/bash
# Script para deploy na AWS Lightsail

set -e

echo "=============================================="
echo "      DEPLOY DO SISTEMA FINANCEIRO GVD"
echo "=============================================="

# Criar estrutura de diretórios
echo "[1/7] Criando estrutura de diretórios..."
mkdir -p logs/nginx backups certbot/conf certbot/www

# Atualizar o sistema
echo "[2/7] Atualizando o sistema..."
sudo apt-get update
sudo apt-get upgrade -y

# Instalar Docker e Docker Compose
echo "[3/7] Instalando Docker e Docker Compose..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    sudo usermod -aG docker $USER
    rm get-docker.sh
fi

if ! command -v docker-compose &> /dev/null; then
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
fi

# Verificar configurações do .env
echo "[4/7] Verificando configurações do .env..."
if [ ! -f .env ]; then
    echo "Arquivo .env não encontrado. Criando a partir do template..."
    cp .env.example .env
    echo "IMPORTANTE: Edite o arquivo .env com as configurações corretas!"
    sleep 3
    nano .env
fi

# Configurar permissões
echo "[5/7] Configurando permissões..."
sudo chmod +x entrypoint.sh
sudo chmod +x setup_db.sh

# Iniciar os serviços
echo "[6/7] Iniciando os serviços Docker..."
docker-compose up -d

# Aguardar inicialização
echo "[7/7] Aguardando inicialização completa..."
sleep 10

# Verificar status
echo "=============================================="
echo "              STATUS DO DEPLOY"
echo "=============================================="
docker-compose ps

echo ""
echo "Deploy concluído com sucesso!"
echo "Sistema acessível em: http://44.197.194.83"
echo ""
echo "Dicas de comandos úteis:"
echo "- Ver logs: docker-compose logs -f"
echo "- Reiniciar todos os serviços: docker-compose restart"
echo "- Parar todos os serviços: docker-compose down"
echo "- Atualizar com novas alterações: git pull && docker-compose up -d --build"