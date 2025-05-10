"""
Middleware customizado para melhorar o tratamento de CSRF
"""
import sys
from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings

# Usar stdout em vez de logging para evitar problemas com arquivos de log
def log_debug(message):
    if settings.DEBUG:
        print(f"[CSRF DEBUG] {message}", file=sys.stderr)

class DebugCsrfMiddleware(CsrfViewMiddleware):
    """
    Middleware de CSRF que fornece mais informações de diagnóstico.
    Esta classe deve ser usada apenas durante a depuração.
    """
    
    def process_view(self, request, callback, callback_args, callback_kwargs):
        """
        Processa a requisição e fornece mais informações sobre erros de CSRF.
        """
        # Log informações úteis para depuração
        if settings.DEBUG:
            log_debug("==== CSRF Debug Info ====")
            log_debug(f"Request path: {request.path}")
            log_debug(f"Request method: {request.method}")
            log_debug(f"Request META: {self._get_relevant_headers(request)}")

            # Verificar cabeçalhos relacionados a CSRF
            csrf_token = request.META.get('HTTP_X_CSRFTOKEN', None)
            csrf_cookie = request.COOKIES.get(settings.CSRF_COOKIE_NAME, None)

            log_debug(f"CSRF Token in header: {csrf_token}")
            log_debug(f"CSRF Cookie: {csrf_cookie}")
            log_debug(f"Host: {request.get_host()}")
            log_debug(f"Origin: {request.META.get('HTTP_ORIGIN', 'None')}")
            log_debug(f"Referer: {request.META.get('HTTP_REFERER', 'None')}")
            log_debug(f"X-Forwarded-Proto: {request.META.get('HTTP_X_FORWARDED_PROTO', 'None')}")
            log_debug(f"Is secure: {request.is_secure()}")
            log_debug(f"CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
        
        # Chamar a implementação original
        return super().process_view(request, callback, callback_args, callback_kwargs)
    
    def _get_relevant_headers(self, request):
        """
        Retorna um dicionário com cabeçalhos HTTP relevantes para diagnóstico.
        """
        relevant_headers = {}
        for key, value in request.META.items():
            if key.startswith('HTTP_') and key not in [
                'HTTP_COOKIE', 'HTTP_HOST', 'HTTP_USER_AGENT'
            ]:
                relevant_headers[key] = value
        
        return relevant_headers