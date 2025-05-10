# Deploy Simplificado no AWS Lightsail

Este guia simplifica o processo de deploy do Sistema GVD no AWS Lightsail, preparando tudo localmente antes de implantar.

**IP público do Lightsail**: 44.197.194.83

## Preparação Local

### 1. Prepare os arquivos de configuração

1. **Altere o docker-compose.yml localmente**:
   - Já alteramos para usar timeout de 120s e 2 workers:
   ```yaml
   command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120
   ```

2. **Altere o nginx.conf localmente**:
   - Já alteramos para usar server_name genérico:
   ```
   server_name _;
   ```

3. **Crie um arquivo .env para o servidor**:
   ```bash
   # No seu ambiente local, crie um arquivo .env.aws
   echo "DEBUG=False
   ALLOWED_HOSTS=44.197.194.83,localhost,127.0.0.1

   DB_USER=financeiro
   DB_DB=financeiro_gvd
   DB_HOST=db
   DB_PORT=5432
   DB_PASSWORD=MinHaSenHaF0rt3

   REDIS_URL=redis://redis:6379/0
   USE_REDIS=True

   # Configurações de email (substitua pelos valores corretos)
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=seu-email@example.com
   EMAIL_HOST_PASSWORD=sua-senha-email
   DEFAULT_FROM_EMAIL=noreply@example.com" > .env.aws
   ```

4. **Crie scripts de manutenção**:
   - Crie um arquivo `backup-db.sh`:
   ```bash
   echo '#!/bin/bash
   BACKUP_DIR="./backups"
   TIMESTAMP=$(date +%Y%m%d%H%M%S)
   mkdir -p $BACKUP_DIR
   docker-compose exec -T db pg_dump -U financeiro -d financeiro_gvd > $BACKUP_DIR/gvd_db_$TIMESTAMP.sql
   gzip $BACKUP_DIR/gvd_db_$TIMESTAMP.sql
   # Manter apenas os últimos 10 backups
   ls -t $BACKUP_DIR/gvd_db_*.sql.gz | tail -n +11 | xargs --no-run-if-empty rm' > backup-db.sh
   
   chmod +x backup-db.sh
   ```

   - Crie um arquivo `monitor.sh`:
   ```bash
   echo '#!/bin/bash
   echo "=== Monitoramento do Sistema GVD ==="
   echo "Data: $(date)"
   echo

   # Verificar status dos contêineres
   echo "=== Status dos Contêineres ==="
   docker-compose ps
   echo

   # Verificar logs recentes do serviço web
   echo "=== Logs Recentes do Serviço Web ==="
   docker-compose logs --tail=20 web
   echo

   # Verificar espaço em disco
   echo "=== Espaço em Disco ==="
   df -h
   echo' > monitor.sh
   
   chmod +x monitor.sh
   ```

5. **Commit as alterações**:
   ```bash
   git add docker-compose.yml nginx.conf backup-db.sh monitor.sh
   git commit -m "Ajustes para deploy no AWS Lightsail"
   git push
   ```

## Processo de Deploy no AWS Lightsail

### 1. Acesso ao Servidor

```bash
ssh ubuntu@44.197.194.83  # ou o usuário correto
```

### 2. Instalação de Docker e Docker Compose

```bash
# Script de instalação completo (copie e cole de uma vez)
sudo apt update && \
sudo apt install -y apt-transport-https ca-certificates curl software-properties-common && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add - && \
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
sudo apt update && \
sudo apt install -y docker-ce docker-compose && \
sudo usermod -aG docker $USER && \
newgrp docker
```

### 3. Clone do Repositório

```bash
# Clone o repositório para a pasta home
cd ~
git clone https://seu-repositorio-git/gvd-system.git
cd gvd-system
```

### 4. Configuração do Ambiente

```bash
# Copie o arquivo .env.aws para .env
cp .env.aws .env

# Crie os diretórios necessários
mkdir -p logs backups
```

### 5. Inicialização dos Contêineres

```bash
# Inicie os contêineres
docker-compose up -d
```

### 6. Verificação do Sistema

```bash
# Verifique o status dos contêineres
docker-compose ps

# Verifique os logs
docker-compose logs -f web
```

### 7. Configuração de Backup Automático

```bash
# Configure o crontab para backup diário às 3h
(crontab -l 2>/dev/null; echo "0 3 * * * cd $HOME/gvd-system && ./backup-db.sh") | crontab -
```

## Solução de Problemas

### Se o sistema não iniciar corretamente:

1. **Verifique os logs**:
   ```bash
   docker-compose logs web
   docker-compose logs db
   ```

2. **Problemas com o banco de dados**:
   ```bash
   # Recrie os volumes (atenção: isso apaga os dados!)
   docker-compose down -v
   docker-compose up -d
   ```

3. **Problemas de permissão**:
   ```bash
   # Corrija as permissões da pasta logs
   sudo chmod -R 777 logs
   ```

## Atualização do Sistema

```bash
# Obtenha as atualizações
git pull

# Reinicie os contêineres
docker-compose down
docker-compose up -d
```

## Configuração de HTTPS (Opcional)

```bash
# Instale o Certbot
sudo apt install -y certbot python3-certbot-nginx

# Configure o certificado para seu domínio
sudo certbot --nginx -d seu-dominio.com
```