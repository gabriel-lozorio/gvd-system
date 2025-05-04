#!/bin/bash
# entrypoint.sh

set -e

# Variables
MAX_RETRIES=30
RETRY_INTERVAL=5

# Functions
function log() {
    echo "[$(date +"%Y-%m-%d %H:%M:%S")] $1"
}

function wait_for_service() {
    local host=$1
    local port=$2
    local service_name=$3
    
    log "Waiting for $service_name at $host:$port..."
    
    local retries=0
    while ! wget -O /dev/null -q "http://$host:$port" >/dev/null 2>&1; do
        retries=$((retries+1))
        if [ $retries -ge $MAX_RETRIES ]; then
            log "Error: $service_name did not become available in time"
            exit 1
        fi
        log "$service_name not available yet. Retrying in $RETRY_INTERVAL seconds... ($retries/$MAX_RETRIES)"
        sleep $RETRY_INTERVAL
    done
    
    log "$service_name is available at $host:$port"
}

# Wait for PostgreSQL
log "Waiting for PostgreSQL..."
until pg_isready -h $POSTGRES_HOST -p $POSTGRES_PORT -U $POSTGRES_USER; do
    log "PostgreSQL not ready yet - sleeping for 5 seconds"
    sleep 5
done
log "PostgreSQL is available now!"

# Wait for Redis if it's being used
if [ -n "$REDIS_URL" ]; then
    REDIS_HOST=$(echo $REDIS_URL | sed -E 's/redis:\/\/([^:]+).*/\1/')
    REDIS_PORT=$(echo $REDIS_URL | sed -E 's/.*:([0-9]+).*/\1/')
    log "Waiting for Redis..."
    wait_for_service $REDIS_HOST $REDIS_PORT "Redis"
fi

# Apply migrations
log "Applying database migrations..."
python manage.py migrate --noinput || { log "Migration failed"; exit 1; }

# Collect static files
log "Collecting static files..."
python manage.py collectstatic --noinput || { log "Static files collection failed"; exit 1; }

# Start application
log "Starting application..."
exec "$@"