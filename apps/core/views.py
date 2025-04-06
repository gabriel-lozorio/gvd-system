# apps/core/views.py

from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from redis.exceptions import RedisError
import redis
from django.conf import settings


def health_check(request):
    """Healthcheck para verificar serviços essenciais"""
    # Verificar banco de dados
    db_ok = True
    try:
        connections['default'].cursor().execute("SELECT 1")
    except OperationalError:
        db_ok = False
    
    # Verificar Redis
    redis_ok = True
    try:
        redis_client = redis.from_url(settings.REDIS_URL)
        redis_client.ping()
    except (RedisError, ConnectionError):
        redis_ok = False
    
    status = {
        'status': 'ok' if db_ok and redis_ok else 'error',
        'database': 'ok' if db_ok else 'error',
        'redis': 'ok' if redis_ok else 'error',
    }
    
    status_code = 200 if status['status'] == 'ok' else 503
    
    return JsonResponse(status, status=status_code)