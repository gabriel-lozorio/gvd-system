#!/usr/bin/env python
"""
Script para depurar problemas de CSRF no Django
"""
import os
import sys
import django
from django.conf import settings

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Exibir configurações relacionadas a CSRF
print("=== Configurações CSRF ===")
print(f"DEBUG: {settings.DEBUG}")
print(f"CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
print(f"CSRF_COOKIE_DOMAIN: {settings.CSRF_COOKIE_DOMAIN}")
print(f"CSRF_USE_SESSIONS: {settings.CSRF_USE_SESSIONS}")
print(f"CSRF_COOKIE_SECURE: {settings.CSRF_COOKIE_SECURE}")
print(f"SESSION_COOKIE_SECURE: {settings.SESSION_COOKIE_SECURE}")
print(f"SECURE_SSL_REDIRECT: {settings.SECURE_SSL_REDIRECT}")
print(f"SECURE_PROXY_SSL_HEADER: {settings.SECURE_PROXY_SSL_HEADER}")
print(f"ALLOWED_HOSTS: {settings.ALLOWED_HOSTS}")

# Verificar middleware
print("\n=== Middleware ===")
csrf_middleware = "django.middleware.csrf.CsrfViewMiddleware" in settings.MIDDLEWARE
print(f"CSRF Middleware encontrado: {csrf_middleware}")
print(f"Posição do CSRF Middleware: {settings.MIDDLEWARE.index('django.middleware.csrf.CsrfViewMiddleware') if csrf_middleware else 'Não encontrado'}")

print("\n=== Dicas para resolução de problemas ===")
print("1. Certifique-se de que o host que você está usando está em CSRF_TRUSTED_ORIGINS")
print("2. Verifique se SECURE_PROXY_SSL_HEADER está configurado corretamente para seu servidor proxy")
print("3. Em desenvolvimento, pode ser necessário definir DEBUG=True e CSRF_COOKIE_SECURE=False")
print("4. Em produção, verifique se os cookies estão sendo configurados corretamente")
print("5. Verifique o Nginx para garantir que os cabeçalhos HTTP corretos estão sendo transmitidos")