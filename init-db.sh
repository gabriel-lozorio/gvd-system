#!/bin/sh
set -e

# Script para inicialização do PostgreSQL
# Este arquivo deve ser montado em /docker-entrypoint-initdb.d/ no container do PostgreSQL

echo "Iniciando configuração do banco de dados..."

# Usar as variáveis de ambiente para criar usuário e banco de dados
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE USER ${DB_USER} WITH PASSWORD '${DB_PASSWORD}';
    CREATE DATABASE ${DB_DB};
    GRANT ALL PRIVILEGES ON DATABASE ${DB_DB} TO ${DB_USER};
    ALTER DATABASE ${DB_DB} OWNER TO ${DB_USER};
EOSQL

echo "Configuração do banco de dados concluída com sucesso!"
echo "Usuário: ${DB_USER}"
echo "Banco: ${DB_DB}"