# Deploy no AWS Lightsail

Este guia detalha o processo de deploy do Sistema GVD no AWS Lightsail.

**IP público do Lightsail**: 50.19.161.72

## Arquivos Preparados Localmente

Os seguintes arquivos já estão configurados e prontos para uso:

- **docker-compose.yml**: Configurado com 2 workers e timeout de 120s
- **nginx.conf**: Configurado com server_name genérico
- **.env.aws**: Arquivo de ambiente para o servidor AWS
- **backup-db.sh**: Script para backup do banco de dados
- **monitor.sh**: Script para monitoramento do sistema

## Passos para o Deploy

### 1. Acesso ao Servidor AWS Lightsail

```bash
ssh ubuntu@50.19.161.72
```

### 2. Instalação do Docker e Docker Compose

```bash
# Instalação completa em um único bloco
sudo apt update && \
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
sudo apt update && \
sudo apt install -y docker-ce docker-compose && \
sudo usermod -aG docker $USER && \
newgrp docker
```

### 3. Clone e Configuração do Repositório

```bash
# Clone o repositório
cd ~
git clone https://seu-repositorio-git/gvd-system.git
cd gvd-system

# Configure o ambiente
cp .env.aws .env
mkdir -p logs backups

# IMPORTANTE: Verifique se a senha do banco de dados está correta no arquivo .env
# A senha correta para o usuário 'financeiro' é: 1eD0hdZz5Lbi
# Se necessário, edite o arquivo:
nano .env
```

### 4. Inicialização do Sistema e Configuração do Django

```bash
# Inicie os contêineres
docker-compose up -d

# Verifique o status
docker-compose ps

# Execute as migrações do Django
docker-compose exec web python manage.py migrate

# Colete arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Crie um superusuário (seguir instruções interativas)
docker-compose exec web python manage.py createsuperuser

# Verifique os logs
docker-compose logs web
```

### 5. Configuração do Backup Automático

```bash
# Configure backup diário às 3h
(crontab -l 2>/dev/null; echo "0 3 * * * cd $HOME/gvd-system && ./backup-db.sh") | crontab -
```

## Verificações Pós-Deploy

### Verificar Acesso ao Sistema

Acesse o sistema via navegador:
- http://50.19.161.72

### Verificar Funcionalidade

- Teste o login
- Verifique se os dados são exibidos corretamente
- Teste a criação de registros

## Solução de Problemas

### Problema: Contêineres não iniciam

```bash
# Verifique os logs
docker-compose logs

# Se necessário, reinicie os contêineres
docker-compose restart
```

### Problema: Banco de dados apresenta erros

```bash
# Verifique logs específicos do banco
docker-compose logs db

# Erro de autenticação com o banco de dados
# Se aparecer "password authentication failed for user 'financeiro'"
# você precisa corrigir o arquivo .env com a senha correta:
nano .env
# Verifique se a senha em DB_PASSWORD está correta (deve ser: 1eD0hdZz5Lbi)
# Salve e reinicie os contêineres:
docker-compose down
docker-compose up -d

# Verificar problemas de migração
docker-compose exec web python manage.py showmigrations

# Tentar rodar as migrações novamente
docker-compose exec web python manage.py migrate

# Em caso de problemas persistentes (⚠️ isso apaga os dados!)
docker-compose down -v
docker-compose up -d
docker-compose exec web python manage.py migrate
```

### Problema: Timeout nos workers

Os ajustes já foram feitos no docker-compose.yml (2 workers e 120s de timeout).
Se ainda ocorrerem problemas:

```bash
docker-compose restart web
```

## Manutenção Contínua

### Atualização do Sistema

```bash
# Faça backup antes de atualizar
./backup-db.sh

# Atualize o código
git pull

# Reinicie os serviços
docker-compose down
docker-compose up -d

# Execute migrações do Django
docker-compose exec web python manage.py migrate

# Atualize arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput
```

### Monitoramento Regular

```bash
# Execute o script de monitoramento
./monitor.sh

# Verifique os logs
docker-compose logs --tail=50
```

### Backup Manual

```bash
# Execute o script de backup
./backup-db.sh
```

## Comandos Django Úteis

### Verificação do Sistema

```bash
# Verificar migrações pendentes
docker-compose exec web python manage.py showmigrations

# Listar URLs disponíveis
docker-compose exec web python manage.py show_urls

# Verificar consistência do banco de dados
docker-compose exec web python manage.py check --database default

# Shell do Django para testes
docker-compose exec web python manage.py shell
```

### Comandos de Manutenção

```bash
# Limpar sessões expiradas
docker-compose exec web python manage.py clearsessions

# Criar backup usando o dumpdata
docker-compose exec web python manage.py dumpdata --exclude auth.permission --exclude contenttypes > data_backup.json
```

## Configuração Adicional (Opcional)

### Configurar HTTPS

```bash
# Instale o Certbot
sudo apt install -y certbot python3-certbot-nginx

# Configure certificado para um domínio
sudo certbot --nginx -d seu-dominio.com
```

### Configurar Firewall

```bash
sudo apt install -y ufw
sudo ufw allow ssh
sudo ufw allow http
sudo ufw allow https
sudo ufw enable
```