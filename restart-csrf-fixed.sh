#!/bin/bash
# Script simplificado para reiniciar o sistema com as correções de CSRF

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}===== Reiniciando GVD System com Correções de CSRF =====${NC}"

# Parar os containers
echo -e "${GREEN}Parando containers...${NC}"
docker-compose down

# Limpar qualquer volume problemático
echo -e "${GREEN}Verificando status do build...${NC}"
docker-compose ps

# Reconstruir o container web
echo -e "${GREEN}Reconstruindo container web...${NC}"
docker-compose build web

# Iniciar o sistema
echo -e "${GREEN}Iniciando o sistema...${NC}"
docker-compose up -d

# Aguardar inicialização
echo -e "${YELLOW}Aguardando inicialização (10s)...${NC}"
sleep 10

# Verificar logs
echo -e "${GREEN}Verificando logs...${NC}"
docker-compose logs --tail=50 web

# Informações finais
echo -e "${YELLOW}===== Sistema Reiniciado =====${NC}"
echo -e "${GREEN}Para testar a funcionalidade CSRF:${NC}"
echo "1. Acesse: https://gvd-system.com.br/core/csrf-test/"
echo "2. Tente enviar o formulário para testar a proteção CSRF"
echo "3. Se tiver problemas, consulte o arquivo CSRF-DEBUG.md"
echo ""
echo -e "${GREEN}Para verificar logs:${NC}"
echo "docker-compose logs -f web | grep -i csrf"