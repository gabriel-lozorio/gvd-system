#!/bin/sh
set -e

echo "Iniciando configuração do banco de dados..."

# Criar o usuário se não existir
psql -v ON_ERROR_STOP=0 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    DO \$\$
    BEGIN
        IF NOT EXISTS (SELECT FROM pg_roles WHERE rolname = '${DB_USER}') THEN
            CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
        END IF;
    END
    \$\$;

    -- Criar o banco financeiro (não financeiro_gvd)
    CREATE DATABASE financeiro;
    GRANT ALL PRIVILEGES ON DATABASE financeiro TO ${DB_USER};
    ALTER DATABASE financeiro OWNER TO ${DB_USER};
EOSQL

echo "Configuração do banco de dados concluída com sucesso!"