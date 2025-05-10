# apps/core/views.py

from django.http import JsonResponse
from django.db import connections
from django.db.utils import OperationalError
from redis.exceptions import RedisError
from django.shortcuts import render
import redis
import json
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


def csrf_test(request):
    """
    View para testar a funcionalidade de CSRF.
    """
    context = {
        'request': request,
        'csrf_cookie_name': settings.CSRF_COOKIE_NAME,
        'csrf_trusted_origins': settings.CSRF_TRUSTED_ORIGINS,
        'csrf_cookie_domain': settings.CSRF_COOKIE_DOMAIN,
    }

    # Verificar se o cookie CSRF existe
    csrf_cookie = request.COOKIES.get(settings.CSRF_COOKIE_NAME, 'Não encontrado')
    context['csrf_cookie_value'] = csrf_cookie

    # Se for um POST, exibir os dados recebidos
    if request.method == 'POST':
        context['submitted_data'] = json.dumps(dict(request.POST), indent=2)

    return render(request, 'csrf_test.html', context)