"""
Configurações específicas para o ambiente AWS Lightsail.
Este arquivo deve ser importado em settings.py para substituir configurações específicas.
"""

# Configurações de segurança otimizadas para AWS Lightsail
ALLOWED_HOSTS = ['gvd-system.com.br', 'www.gvd-system.com.br', '50.19.161.72', 'localhost', '127.0.0.1']

# Configuração otimizada de CSRF para Lightsail
CSRF_TRUSTED_ORIGINS = [
    'https://gvd-system.com.br',
    'https://www.gvd-system.com.br',
    'http://gvd-system.com.br',
    'http://www.gvd-system.com.br',
    'http://50.19.161.72',
    'https://50.19.161.72',
]

# Configurações de proxy e segurança
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_SSL_REDIRECT = True

# Em caso de problemas, você pode definir temporariamente:
# CSRF_COOKIE_SECURE = False
# SESSION_COOKIE_SECURE = False
# SECURE_SSL_REDIRECT = False

# Use sessões para CSRF
CSRF_USE_SESSIONS = True
CSRF_COOKIE_HTTPONLY = False  # Precisa ser False para permitir acesso JS
CSRF_COOKIE_SAMESITE = 'Lax'  # Use 'Lax' para permitir navegação de terceiros

# Armazene o cookie apenas para este domínio
CSRF_COOKIE_DOMAIN = None  # Definido automaticamente com base no host da requisição