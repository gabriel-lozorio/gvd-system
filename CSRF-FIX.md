# Correção do erro de verificação CSRF no GVD System

Este documento descreve as correções aplicadas para resolver o problema de verificação CSRF que ocorria após a configuração do HTTPS.

## Problema diagnosticado

O erro principal estava na tentativa de usar `config.settings.production` quando a estrutura real do projeto não contém um pacote settings/ dentro do diretório config/. Os arquivos base.py e production.py estavam no lugar incorreto e não eram encontrados pelo sistema.

## Alterações aplicadas

1. **Reversão do DJANGO_SETTINGS_MODULE**:
   - Alterado de volta para `config.settings` em vez de `config.settings.production`
   - Este é o caminho correto para o arquivo de configuração do Django neste projeto

2. **Configurações CSRF no arquivo principal settings.py**:
   - Adicionadas todas as origens confiáveis, incluindo HTTP e HTTPS
   - Removido o CSRF_COOKIE_DOMAIN fixo para usar o domínio da requisição
   - Configurado CSRF_USE_SESSIONS para armazenar tokens na sessão
   - Adicionado SECURE_PROXY_SSL_HEADER para reconhecer HTTPS por trás do proxy

3. **Configuração de DEBUG dinâmico**:
   - DEBUG agora usa a variável de ambiente para determinar o modo de execução
   - Por padrão, o modo de produção será ativado (DEBUG=False)

4. **Headers NGINX**:
   - A configuração do NGINX foi atualizada para transmitir corretamente todos os cabeçalhos HTTP necessários
   - Adicionado header Origin para garantir que o CSRF reconheça corretamente o domínio

## Como testar as alterações

1. Reinicie o stack Docker com os novos arquivos:
   ```bash
   docker-compose down
   docker-compose up -d
   ```

2. Verifique os logs para garantir que não há erros:
   ```bash
   docker-compose logs -f web
   ```

3. Tente acessar o sistema via HTTPS e verificar se as operações que requerem CSRF (login, formulários, etc.) funcionam corretamente.

4. Se ainda houver problemas:
   - Verifique os logs de erro do Django
   - Use as ferramentas do navegador para inspecionar os cabeçalhos da requisição e o cookie CSRF
   - Verifique se o header `Origin` está sendo enviado corretamente
   - Confirme que o domínio nos cabeçalhos da resposta corresponde ao da requisição

## Depuração adicional

Para depurar problemas de CSRF, você pode adicionar temporariamente o seguinte ao settings.py:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.security.csrf': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
```

Isso registrará informações detalhadas sobre o processamento CSRF no console.