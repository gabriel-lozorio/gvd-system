# Configuração do Sistema GVD

Este documento contém informações sobre a configuração atual do sistema.

## Arquivos de Configuração

Os principais arquivos de configuração são:

- `docker-compose.yml` - Configuração dos serviços Docker
- `Dockerfile` - Configuração da imagem Docker
- `nginx.conf` - Configuração do servidor Nginx
- `.env` - Variáveis de ambiente (não versionado)

## Alterações Realizadas

As seguintes alterações foram feitas para melhorar o desempenho:

1. **Timeout do Gunicorn**: Alterado para 120 segundos e reduzido para 2 workers
   - Arquivo: `docker-compose.yml`
   - Configuração: `command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120`

2. **Configuração do Nginx**: Configurado para aceitar qualquer servidor
   - Arquivo: `nginx.conf`
   - Configuração: `server_name _;` (antes era IP fixo)

## Monitoramento e Backup

Serão configurados durante o deploy no AWS Lightsail:

- Script de backup diário do banco de dados
- Script de monitoramento para verificar o estado do sistema

## Documentação

A documentação completa do deploy está no arquivo `DEPLOY-STEPS.md`, com instruções
passo a passo para configurar o sistema no AWS Lightsail.

## Próximos Passos

1. Realizar o deploy no AWS Lightsail seguindo as instruções
2. Configurar HTTPS após o deploy
3. Implementar backups automáticos
4. Configurar monitoramento contínuo