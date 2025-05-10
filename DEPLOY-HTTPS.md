# Configuração HTTPS para o Sistema Financeiro GVD

Este guia explica como configurar HTTPS no seu servidor para o Sistema Financeiro GVD.

## Pré-requisitos

- Um nome de domínio configurado e apontando para o IP do seu servidor
- Acesso via SSH ao servidor
- Docker e Docker Compose instalados e funcionando
- Sistema já implantado e funcionando em HTTP

## Passo 1: Obter Certificados SSL com Certbot ✅

Certbot é a ferramenta oficial da EFF para obtenção de certificados Let's Encrypt, que são gratuitos e válidos por 90 dias (com renovação automática).

```bash
# Instalar Certbot (se já não estiver instalado)
sudo apt-get update
sudo apt-get install certbot

# Parar os contêineres Docker para liberar as portas (se necessário)
cd ~/gvd/gvd-system && docker-compose down

# Obter o certificado usando o modo standalone
sudo certbot certonly --standalone -d gvd-system.com.br -d www.gvd-system.com.br
```

✅ **CONCLUÍDO**: Os certificados foram instalados com sucesso em `/etc/letsencrypt/live/gvd-system.com.br/`.
O Certbot configurou automaticamente a renovação através de um cronjob.

**Importante**: Não adicione os certificados ao controle de versão. O arquivo `.gitignore` foi atualizado para excluir certificados e configurações locais.

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
# Reiniciar os contêineres Docker
cd ~/gvd/gvd-system
docker-compose up -d
```

Isso irá iniciar os contêineres com a nova configuração HTTPS. O NGINX carregará os certificados SSL que o Certbot gerou.

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