# Solução Correta para o Deploy no AWS

Parece que estamos enfrentando um problema de configuração do banco de dados. Vamos resolver de forma limpa, sem configurações manuais:

## 1. Verificação do arquivo .env

Garanta que o arquivo `.env` tenha exatamente este conteúdo:

```
DEBUG=False
ALLOWED_HOSTS=50.19.161.72,localhost,127.0.0.1

DB_USER=financeiro
DB_DB=financeiro_gvd
DB_HOST=db
DB_PORT=5432
DB_PASSWORD=1eD0hdZz5Lbi

REDIS_URL=redis://redis:6379/0
USE_REDIS=True

EMAIL_HOST=smtp.example.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=seu-email@example.com
EMAIL_HOST_PASSWORD=sua-senha-email
DEFAULT_FROM_EMAIL=noreply@example.com
```

## 2. Limpar completamente tudo e começar do zero

```bash
# Pare todos os serviços
docker-compose down

# Remova todos os volumes (isso eliminará todos os dados!)
docker volume rm $(docker volume ls -q | grep gvd-system)

# Verifique se todos os volumes foram removidos
docker volume ls

# Remova imagens antigas para garantir build limpo
docker rmi $(docker images -q gvd-system_web gvd-system_celery gvd-system_celery-beat)

# Inicie tudo novamente
docker-compose up -d

# Aguarde 30 segundos para garantir que o banco de dados inicialize completamente
sleep 30

# Verifique o status
docker-compose ps
```

## 3. Verificar as variáveis usadas pelo banco de dados

```bash
# Verifique as variáveis de ambiente no contêiner do PostgreSQL
docker-compose exec db env | grep POSTGRES
```

Deve mostrar:
```
POSTGRES_USER=financeiro
POSTGRES_PASSWORD=1eD0hdZz5Lbi
POSTGRES_DB=financeiro_gvd
```

## 4. Execute as migrações do Django

```bash
# Execute as migrações
docker-compose exec web python manage.py migrate

# Colete os arquivos estáticos
docker-compose exec web python manage.py collectstatic --noinput

# Crie um superusuário
docker-compose exec web python manage.py createsuperuser
```

## 5. Teste o sistema

Acesse o sistema pelo navegador:
```
http://50.19.161.72
```

## Problemas Conhecidos

### Se você ver erro sobre banco "financeiro" não existir:

O erro "database 'financeiro' does not exist" significa que o Django está procurando um banco com nome diferente do que criamos. Nesse caso, você precisa:

1. Verificar o nome do banco especificado no `.env` (deve ser `financeiro_gvd`)
2. Verificar se a variável `DB_NAME` está sendo usada em algum lugar que deveria ser `DB_DB`

Corrija isso editando o arquivo de configuração do Django:

```bash
docker-compose exec web cat /app/config/settings.py | grep DATABASE
```

Se necessário:

```bash
docker-compose exec web bash
cd /app
grep -r "DB_NAME" --include="*.py" .
```