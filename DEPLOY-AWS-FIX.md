# Correção de Problemas com o Banco de Dados no AWS

Este documento contém passos para resolver o problema de autenticação do banco de dados.

## Solução 1: Verificar as Variáveis de Ambiente nos Contêineres

Execute os seguintes comandos no servidor:

```bash
# Verifique as variáveis de ambiente no contêiner web
docker-compose exec web env | grep DB_

# Verifique as variáveis de ambiente no contêiner db
docker-compose exec db env | grep POSTGRES
```

## Solução 2: Recriar o Banco de Dados com a Senha Correta

Se as variáveis estiverem incorretas, recrie os contêineres:

```bash
# Pare todos os contêineres
docker-compose down

# Remova os volumes (isso apagará os dados!)
docker volume ls | grep gvd
docker volume rm gvd-system_postgres_data

# Certifique-se que o .env está com o conteúdo correto:
cat > .env << EOF
DEBUG=False
ALLOWED_HOSTS=44.197.194.83,localhost,127.0.0.1

DB_USER=financeiro
DB_DB=financeiro_gvd
DB_HOST=db
DB_PORT=5432
DB_PASSWORD=1eD0hdZz5Lbi

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

# Inicie os contêineres novamente
docker-compose up -d

# Verifique os logs do banco de dados
docker-compose logs db

# Teste a conexão com o banco
docker-compose exec db psql -U financeiro -d financeiro_gvd -c "SELECT 1;"

# Execute as migrações do Django
docker-compose exec web python manage.py migrate
```

## Solução 3: Verificar configuração do PostgreSQL

```bash
# Entre no contêiner do PostgreSQL
docker-compose exec db bash

# Verifique a configuração de autenticação
cat /var/lib/postgresql/data/pg_hba.conf

# Verifique usuários e senhas
psql -U postgres
\du
\q

# Saia do contêiner
exit
```

## Solução 4: Criar usuário manualmente no PostgreSQL

```bash
# Entre no PostgreSQL como usuário postgres
docker-compose exec db psql -U postgres

# Crie ou altere o usuário financeiro
CREATE USER financeiro WITH PASSWORD '1eD0hdZz5Lbi';
ALTER USER financeiro WITH PASSWORD '1eD0hdZz5Lbi';

# Crie o banco de dados se necessário
CREATE DATABASE financeiro_gvd;

# Dê permissões ao usuário
GRANT ALL PRIVILEGES ON DATABASE financeiro_gvd TO financeiro;

# Saia do PostgreSQL
\q

# Tente conectar com o usuário financeiro
docker-compose exec db psql -U financeiro -d financeiro_gvd

# Saia do cliente PostgreSQL
\q

# Tente executar as migrações novamente
docker-compose exec web python manage.py migrate
```

## Solução 5: Usar Docker Compose Override

Crie um arquivo docker-compose.override.yml para sobrescrever as credenciais do banco de dados:

```bash
cat > docker-compose.override.yml << EOF
version: '3.8'

services:
  db:
    environment:
      - POSTGRES_USER=financeiro
      - POSTGRES_PASSWORD=1eD0hdZz5Lbi
      - POSTGRES_DB=financeiro_gvd
EOF

# Reinicie os contêineres com as novas configurações
docker-compose down
docker-compose up -d

# Verifique se as variáveis foram aplicadas
docker-compose exec db env | grep POSTGRES

# Tente as migrações novamente
docker-compose exec web python manage.py migrate
```