#!/bin/bash
# setup_db.sh - Create database and user using environment variables

set -e

# Load variables from .env if available
if [ -f .env ]; then
    source .env
fi

# Check required variables
if [ -z "$POSTGRES_DB" ] || [ -z "$POSTGRES_USER" ] || [ -z "$POSTGRES_PASSWORD" ]; then
    echo "Error: Missing required environment variables. Please set POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD"
    exit 1
fi

# Create database and user
psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    CREATE DATABASE $POSTGRES_DB;
    CREATE USER $POSTGRES_USER WITH PASSWORD '$POSTGRES_PASSWORD';
    ALTER ROLE $POSTGRES_USER SET client_encoding TO 'utf8';
    ALTER ROLE $POSTGRES_USER SET timezone TO 'America/Sao_Paulo';
    GRANT ALL PRIVILEGES ON DATABASE $POSTGRES_DB TO $POSTGRES_USER;
EOSQL

echo "Database setup completed successfully!"