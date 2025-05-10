# Diagnóstico e Solução de Problemas CSRF no GVD System

Este guia de solução de problemas ajudará a diagnosticar e resolver problemas de verificação CSRF que podem ocorrer ao acessar o sistema via HTTPS.

## Ferramentas de diagnóstico implementadas

1. **Middleware Debug CSRF**
   - Substitui o middleware padrão do Django para fornecer mais informações sobre falhas de CSRF
   - Disponível em `apps/core/middleware.py`
   - Ativado automaticamente quando `DEBUG = True`

2. **Página de teste CSRF**
   - URL: `/core/csrf-test/`
   - Exibe informações detalhadas sobre a configuração CSRF
   - Permite testar formulários POST para verificar se a proteção CSRF está funcionando

3. **Script de diagnóstico Python**
   - Arquivo: `debug-csrf.py`
   - Exibe configurações atuais do Django relacionadas a CSRF
   - Execute: `python debug-csrf.py`

4. **Scripts de diagnóstico de rede**
   - Arquivo: `test-csrf.sh`
   - Testa a acessibilidade do site e verifica cabeçalhos HTTP

## Como diagnosticar problemas CSRF

### 1. Verificar configurações atuais

```bash
# Ative o modo DEBUG
nano .env
# Altere DEBUG=False para DEBUG=True

# Reinicie os contêineres
docker-compose down
docker-compose up -d

# Execute o diagnóstico
docker-compose exec web python /app/debug-csrf.py
```

### 2. Testar com a página de teste CSRF

Acesse: `https://gvd-system.com.br/core/csrf-test/`

Esta página permitirá:
- Ver se o cookie CSRF está sendo definido corretamente
- Verificar se o sistema aceita formulários POST com o token CSRF
- Inspecionar os cabeçalhos HTTP relacionados

### 3. Verificar logs para erros CSRF

```bash
docker-compose logs web | grep -i csrf
```

## Soluções para problemas comuns

### Problema: CSRF cookie não está sendo definido

**Solução**:
1. Certifique-se de que o cabeçalho `Set-Cookie` está presente nas respostas
2. Verifique se `CSRF_COOKIE_SECURE = True` está configurado corretamente para HTTPS
3. Para testar localmente, defina `CSRF_COOKIE_SECURE = False` temporariamente

### Problema: CSRF verification failed. Request aborted

**Solução**:
1. Verifique se o domínio que você está usando está em `CSRF_TRUSTED_ORIGINS`
2. Certifique-se de que o cabeçalho `Origin` ou `Referer` está sendo enviado pelo navegador
3. Verifique se o cabeçalho `X-Forwarded-Proto` está sendo passado corretamente pelo Nginx

### Problema: CSRF verification failed - HTTPS vs HTTP

**Solução**:
1. Certifique-se de que `SECURE_PROXY_SSL_HEADER` está definido corretamente
2. No Nginx, confirme que `proxy_set_header X-Forwarded-Proto $scheme;` está presente
3. Adicione cabeçalhos de debug para ver o que está sendo recebido pelo Django:
   ```
   add_header X-Debug-Proto $scheme;
   add_header X-Debug-Host $host;
   ```

## Configurações alternativas para testar

Se ainda estiver tendo problemas, tente estas configurações alternativas:

### Opção 1: Desabilitar CSRF temporariamente

> ⚠️ Use apenas para diagnóstico, NUNCA em produção!

Em `settings.py`, remova temporariamente o middleware CSRF:
```python
MIDDLEWARE = [
    # ... outros middlewares ...
    # 'django.middleware.csrf.CsrfViewMiddleware',  # Comentado para diagnóstico
    # ... outros middlewares ...
]
```

### Opção 2: Usar apenas HTTP para diagnóstico

1. Defina `SECURE_SSL_REDIRECT = False` em settings.py
2. Use HTTP em vez de HTTPS para acessar o site (temporariamente)
3. Verifique se o problema persiste

### Opção 3: Modificar configurações de cookie

```python
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_DOMAIN = None
CSRF_COOKIE_SAMESITE = 'Lax'  # Tente 'None' se ainda tiver problemas
SESSION_COOKIE_SECURE = False
```

## Referências

Para mais informações sobre CSRF no Django, consulte:
- [Documentação oficial do Django sobre CSRF](https://docs.djangoproject.com/en/4.2/ref/csrf/)
- [Cabeçalhos HTTP para CSRF](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-CSRF-Token)
- [SameSite Cookie Attribute](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite)