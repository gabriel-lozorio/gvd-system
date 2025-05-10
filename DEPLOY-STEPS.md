# Deploy do Sistema GVD no AWS Lightsail

Este documento contém o passo a passo completo para realizar o deploy do Sistema GVD no AWS Lightsail.

**IP público do Lightsail**: 44.197.194.83

## 1. Acesso e Configuração Inicial do Servidor Lightsail

1. **Conecte-se ao servidor via SSH**:
   ```bash
   ssh ubuntu@44.197.194.83  # ou use o usuário adequado (admin, ec2-user, etc.)
   ```

2. **Atualize o sistema**:
   ```bash
   sudo apt update
   sudo apt upgrade -y
   ```

3. **Instale o Docker e Docker Compose**:
   ```bash
   # Instale as dependências
   sudo apt install -y apt-transport-https ca-certificates curl software-properties-common

   # Adicione a chave GPG do Docker
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

   # Adicione o repositório do Docker
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"

   # Atualize e instale o Docker
   sudo apt update
   sudo apt install -y docker-ce docker-compose

   # Adicione seu usuário ao grupo docker
   sudo usermod -aG docker $USER

   # Aplique as alterações de grupo sem fazer logout
   newgrp docker
   ```

4. **Verifique a instalação do Docker**:
   ```bash
   docker --version
   docker-compose --version
   ```

## 2. Clone e Configuração do Projeto

1. **Clone o repositório**:
   ```bash
   # Crie um diretório para o projeto
   mkdir -p /home/ubuntu/gvd
   cd /home/ubuntu/gvd

   # Clone o repositório (substitua pelo URL correto)
   git clone https://seu-repositorio-git/gvd-system.git
   cd gvd-system
   ```

2. **Configure o arquivo .env**:
   ```bash
   # Crie o arquivo .env
   cat > .env << EOF
   DEBUG=False
   ALLOWED_HOSTS=44.197.194.83,localhost,127.0.0.1

   DB_USER=financeiro
   DB_DB=financeiro_gvd
   DB_HOST=db
   DB_PORT=5432
   # Use uma senha forte aqui
   DB_PASSWORD=$(openssl rand -base64 12)

   REDIS_URL=redis://redis:6379/0
   USE_REDIS=True

   # Configurações de email (substitua pelos valores corretos)
   EMAIL_HOST=smtp.example.com
   EMAIL_PORT=587
   EMAIL_USE_TLS=True
   EMAIL_HOST_USER=seu-email@example.com
   EMAIL_HOST_PASSWORD=sua-senha-email
   DEFAULT_FROM_EMAIL=noreply@example.com
   EOF
   ```

3. **Atualize o nginx.conf**:
   ```bash
   # Edite o arquivo nginx.conf
   sed -i 's/server_name 44.197.194.83;/server_name _;/' nginx.conf
   ```

4. **Atualize o docker-compose.yml**:
   ```bash
   # Substitua a configuração do Gunicorn para melhorar o timeout
   sed -i 's/command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4/command: gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120/' docker-compose.yml
   ```

## 3. Inicialização do Sistema

1. **Crie diretórios necessários**:
   ```bash
   mkdir -p logs backups
   chmod 777 logs
   ```

2. **Inicie os contêineres**:
   ```bash
   docker-compose up -d
   ```

3. **Verifique o status dos contêineres**:
   ```bash
   docker-compose ps
   ```

4. **Verifique os logs para garantir que tudo está funcionando**:
   ```bash
   docker-compose logs -f web
   ```

## 4. Configuração do Banco de Dados (Se Necessário)

1. **Verifique se há erros no banco de dados**:
   ```bash
   docker-compose logs db
   ```

2. **Problema comum**: Se o banco de dados estiver com erro de autenticação ou tiver problemas, pode ser necessário recriá-lo:
   ```bash
   # Pare os contêineres
   docker-compose down

   # Remova os volumes e inicie novamente 
   # (Cuidado: isso apagará os dados existentes!)
   docker-compose down -v
   docker-compose up -d
   ```

## 5. Verificação Final

1. **Teste o acesso ao sistema**:
   ```bash
   curl -I http://localhost
   ```

2. **Verifique se o sistema está acessível pelo IP público**:
   - Abra um navegador e acesse: http://44.197.194.83

## 6. Configuração de Backup

1. **Crie um script de backup**:
   ```bash
   cat > backup-db.sh << 'EOF'
   #!/bin/bash
   BACKUP_DIR="./backups"
   TIMESTAMP=$(date +%Y%m%d%H%M%S)
   mkdir -p $BACKUP_DIR
   docker-compose exec -T db pg_dump -U financeiro -d financeiro_gvd > $BACKUP_DIR/gvd_db_$TIMESTAMP.sql
   gzip $BACKUP_DIR/gvd_db_$TIMESTAMP.sql
   # Manter apenas os últimos 10 backups
   ls -t $BACKUP_DIR/gvd_db_*.sql.gz | tail -n +11 | xargs --no-run-if-empty rm
   EOF

   chmod +x backup-db.sh
   ```

2. **Configure o backup automático**:
   ```bash
   # Adicione ao crontab para executar diariamente às 3h da manhã
   (crontab -l 2>/dev/null; echo "0 3 * * * cd /home/ubuntu/gvd/gvd-system && ./backup-db.sh") | crontab -
   ```

## 7. Configuração de Monitoramento

1. **Crie um script de monitoramento**:
   ```bash
   cat > monitor.sh << 'EOF'
   #!/bin/bash
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
   echo
   EOF

   chmod +x monitor.sh
   ```

## 8. Configuração de Segurança

1. **Configure HTTPS (recomendado)**:
   ```bash
   # Instale o Certbot
   sudo apt install -y certbot python3-certbot-nginx

   # Obtenha e configure certificado SSL
   sudo certbot --nginx -d 44.197.194.83.nip.io

   # Nota: Para usar um domínio real, substitua 44.197.194.83.nip.io pelo seu domínio
   ```

2. **Configure o firewall**:
   ```bash
   # Verifique se o UFW está instalado
   sudo apt install -y ufw

   # Configure as regras
   sudo ufw allow ssh
   sudo ufw allow http
   sudo ufw allow https

   # Ative o firewall
   sudo ufw enable
   ```

## 9. Manutenção e Atualização

### Para atualizar o sistema:

```bash
# Faça backup do banco de dados
./backup-db.sh

# Atualize o código do repositório
git pull

# Reinicie os contêineres
docker-compose down
docker-compose up -d
```

### Para reiniciar o sistema:

```bash
# Reinicie todos os serviços
docker-compose restart

# Ou apenas um serviço específico
docker-compose restart web
```

## 10. Solução de Problemas Comuns

### Problema 1: Timeouts nos workers
Se você ver mensagens "WORKER TIMEOUT" nos logs:

```bash
# Edite docker-compose.yml e aumente o timeout
# Já configuramos para 120 segundos, mas pode ser necessário aumentar mais
```

### Problema 2: Erro de conexão com o banco de dados
Verifique se as credenciais no arquivo .env estão corretas e se o banco de dados está em execução:

```bash
# Verifique os logs do banco de dados
docker-compose logs db

# Reinicie apenas o banco de dados
docker-compose restart db
```

### Problema 3: Erro na migração do banco de dados
Se houver erros nas migrações:

```bash
# Execute as migrações manualmente
docker-compose exec web python manage.py migrate
```

## 11. Acesso ao Sistema

Após a instalação, acesse o sistema pelo navegador:
- URL: http://44.197.194.83
- Após configurar HTTPS: https://44.197.194.83

Você será redirecionado para a tela de login.