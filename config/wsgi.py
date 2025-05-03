import os
from django.core.wsgi import get_wsgi_application

# Configuração para ambiente de produção por padrão
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
application = get_wsgi_application()