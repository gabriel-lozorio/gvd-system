"""
Middleware customizado para melhorar o tratamento de CSRF
"""
import logging
from django.middleware.csrf import CsrfViewMiddleware
from django.conf import settings

logger = logging.getLogger('django.security.csrf')

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
            logger.debug("==== CSRF Debug Info ====")
            logger.debug(f"Request path: {request.path}")
            logger.debug(f"Request method: {request.method}")
            logger.debug(f"Request META: {self._get_relevant_headers(request)}")
            
            # Verificar cabeçalhos relacionados a CSRF
            csrf_token = request.META.get('HTTP_X_CSRFTOKEN', None)
            csrf_cookie = request.COOKIES.get(settings.CSRF_COOKIE_NAME, None)
            
            logger.debug(f"CSRF Token in header: {csrf_token}")
            logger.debug(f"CSRF Cookie: {csrf_cookie}")
            logger.debug(f"Host: {request.get_host()}")
            logger.debug(f"Origin: {request.META.get('HTTP_ORIGIN', 'None')}")
            logger.debug(f"Referer: {request.META.get('HTTP_REFERER', 'None')}")
            logger.debug(f"X-Forwarded-Proto: {request.META.get('HTTP_X_FORWARDED_PROTO', 'None')}")
            logger.debug(f"Is secure: {request.is_secure()}")
            logger.debug(f"CSRF_TRUSTED_ORIGINS: {settings.CSRF_TRUSTED_ORIGINS}")
        
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