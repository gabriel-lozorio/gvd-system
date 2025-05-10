# Correção do erro de verificação CSRF em HTTPS

Este documento descreve as alterações feitas para corrigir o erro de verificação CSRF que ocorre ao acessar o sistema via HTTPS.

## Alterações realizadas

1. **Modificação do arquivo wsgi.py**:
   - Atualizado para usar explicitamente as configurações de produção (`config.settings.production`).

2. **Atualização das configurações CSRF em production.py**:
   - Adicionados hosts HTTP aos origins confiáveis
   - Configurado o domínio de cookie CSRF para incluir subdomínios
   - Habilitado o armazenamento de tokens CSRF em sessões

3. **Atualização do arquivo .env**:
   - Definido `DEBUG=False` para garantir que o ambiente de produção seja usado

4. **Modificação do docker-compose.yml**:
   - Adicionada variável de ambiente `DJANGO_SETTINGS_MODULE=config.settings.production`

5. **Atualização da configuração do NGINX**:
   - Adicionados headers adicionais para proxy reverso, incluindo Origin, X-Forwarded-Host e X-Forwarded-Port

6. **Atualização do settings.py principal**:
   - Replicadas as configurações CSRF de produção para maior compatibilidade

## Instruções para implantação

1. Faça backup dos arquivos modificados:
   ```bash
   cp config/wsgi.py config/wsgi.py.bak
   cp config/settings/production.py config/settings/production.py.bak
   cp .env .env.bak
   cp docker-compose.yml docker-compose.yml.bak
   cp nginx.conf nginx.conf.bak
   cp config/settings.py config/settings.py.bak
   ```

2. Aplique as alterações conforme descrito acima.

3. Reconstrua e reinicie os contêineres Docker:
   ```bash
   docker-compose down
   docker-compose build web
   docker-compose up -d
   ```

4. Verifique os logs para identificar possíveis erros:
   ```bash
   docker-compose logs -f web
   ```

5. Teste o acesso HTTPS ao sistema para confirmar que os problemas de CSRF foram resolvidos.

## Solução de problemas

Se o problema persistir após estas alterações, verifique:

1. **Logs do Django**:
   - Examine os logs para mensagens de erro detalhadas relacionadas a CSRF
   - Verifique quais configurações estão sendo carregadas: `docker-compose exec web python -c "import os; print(os.environ.get('DJANGO_SETTINGS_MODULE'))"`

2. **Cabeçalhos HTTP**:
   - Use ferramentas como cURL ou as ferramentas de desenvolvedor do navegador para verificar os cabeçalhos enviados nas requisições
   - Confirme que o cabeçalho `Origin` corresponde a um dos valores em `CSRF_TRUSTED_ORIGINS`

3. **Cookies**:
   - Verifique se o cookie CSRF está sendo definido corretamente no navegador
   - Confirme que o domínio do cookie está correto

4. **Limpeza de cache**:
   - Limpe o cache e os cookies do navegador
   - Tente acessar em um navegador diferente ou em modo anônimo