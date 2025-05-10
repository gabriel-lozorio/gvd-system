# Configuração HTTPS para o Sistema Financeiro GVD

Este guia explica como configurar HTTPS no seu servidor para o Sistema Financeiro GVD.

## Pré-requisitos

- Um nome de domínio configurado e apontando para o IP do seu servidor
- Acesso via SSH ao servidor
- Docker e Docker Compose instalados e funcionando
- Sistema já implantado e funcionando em HTTP

## Passo 1: Obter Certificados SSL com Certbot

Certbot é a ferramenta oficial da EFF para obtenção de certificados Let's Encrypt, que são gratuitos e válidos por 90 dias (com renovação automática).

```bash
# Instalar Certbot (se já não estiver instalado)
sudo apt-get update
sudo apt-get install certbot

# Criar pasta para validação do Certbot
sudo mkdir -p /var/www/html/.well-known/acme-challenge

# Obter o certificado usando o modo standalone (temporariamente pára seu servidor web)
sudo systemctl stop docker-compose@gvd-system  # Se estiver usando systemd
# OU
cd /home/seu-usuario/gvd-system && docker-compose down  # Se estiver gerenciando manualmente

# Obter o certificado
sudo certbot certonly --standalone -d gvd-system.com.br -d www.gvd-system.com.br

# Se preferir o modo webroot (não precisa parar o servidor)
# sudo certbot certonly --webroot -w /var/www/html -d gvd-system.com.br -d www.gvd-system.com.br
```

## Passo 2: Configurar o NGINX (já feito)

O arquivo nginx.conf já foi configurado para HTTPS. As principais mudanças foram:

1. Redirecionamento de HTTP para HTTPS
2. Configuração dos certificados SSL
3. Configurações de segurança recomendadas para SSL/TLS

## Passo 3: Configurar o Django (já feito)

O arquivo config/settings/production.py já foi atualizado para suportar HTTPS:

1. Ativação dos redirecionamentos SSL
2. Configuração de cookies seguros
3. Configuração de cabeçalhos de segurança HTTPS

## Passo 4: Reiniciar os Serviços

```bash
# Se você usa systemd
sudo systemctl restart docker-compose@gvd-system

# OU manualmente
cd /home/seu-usuario/gvd-system
docker-compose down
docker-compose up -d
```

## Passo 5: Testar o HTTPS

1. Acesse o site via HTTPS: https://gvd-system.com.br
2. Verifique se o redirecionamento de HTTP para HTTPS está funcionando
3. Verifique se o certificado é válido (cadeado verde no navegador)

## Solução de Problemas

### Certificado não é renovado automaticamente

Configure um cronjob para renovação automática:

```bash
# Editar o crontab
sudo crontab -e

# Adicionar esta linha para verificar renovação duas vezes por dia
0 0,12 * * * certbot renew --quiet --post-hook "docker restart gvd-system_nginx_1"
```

### Problemas com a validação do Let's Encrypt

Certifique-se de que:
- O domínio está configurado corretamente e aponta para o servidor
- A porta 80 está aberta durante a validação
- O diretório .well-known/acme-challenge está acessível publicamente

### Erros de NGINX com SSL

Verifique os logs do NGINX:

```bash
docker-compose logs nginx
```

## Verificação de Segurança

Após a configuração, você pode verificar a segurança do seu site usando:

- [SSL Labs Server Test](https://www.ssllabs.com/ssltest/)
- [Security Headers](https://securityheaders.com/)

## Renovação Manual dos Certificados

Se precisar renovar manualmente:

```bash
sudo certbot renew --force-renewal
docker restart gvd-system_nginx_1
```