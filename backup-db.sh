#!/bin/bash
# Script para backup do banco de dados PostgreSQL
BACKUP_DIR="./backups"
TIMESTAMP=$(date +%Y%m%d%H%M%S)
mkdir -p $BACKUP_DIR
docker-compose exec -T db pg_dump -U financeiro -d financeiro_gvd > $BACKUP_DIR/gvd_db_$TIMESTAMP.sql
gzip $BACKUP_DIR/gvd_db_$TIMESTAMP.sql
# Manter apenas os últimos 10 backups
ls -t $BACKUP_DIR/gvd_db_*.sql.gz | tail -n +11 | xargs --no-run-if-empty rm