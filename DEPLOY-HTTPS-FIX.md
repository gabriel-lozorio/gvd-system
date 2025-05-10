# Correção do erro de verificação CSRF em HTTPS

Este documento descreve as alterações feitas para corrigir o erro de verificação CSRF que ocorre ao acessar o sistema via HTTPS.

## Problema encontrado

O principal problema identificado foi que estávamos tentando usar `config.settings.production`, mas a estrutura do projeto não está organizada dessa forma. O sistema está configurado para usar diretamente `config.settings.py` em vez de um pacote settings/.

## Alterações realizadas

1. **Reversão do arquivo wsgi.py**:
   - Revertido para usar as configurações padrão (`config.settings`) em vez de tentar carregar um módulo inexistente.

2. **Atualização das configurações CSRF no settings.py principal**:
   - Adicionados hosts HTTP e HTTPS aos origins confiáveis
   - Configurado o domínio de cookie CSRF para ser determinado automaticamente pelo Django
   - Habilitado o armazenamento de tokens CSRF em sessões
   - Adicionado o cabeçalho de proxy SSL para reconhecer requisições HTTPS

3. **Melhoria na configuração de DEBUG**:
   - Configurado para usar a variável de ambiente `DEBUG` do arquivo .env
   - Por padrão será False se não for especificado, garantindo que o modo de produção seja usado

4. **Modificação do docker-compose.yml**:
   - Ajustada variável de ambiente `DJANGO_SETTINGS_MODULE` para apontar para o arquivo correto

5. **Atualização da configuração do NGINX**:
   - Adicionados cabeçalhos adicionais para proxy reverso, incluindo Origin, X-Forwarded-Host e X-Forwarded-Port

6. **Adição de logs avançados**:
   - Configuração de logging específica para depuração de problemas de CSRF
   - Os logs serão gravados em arquivo e no console para facilitar a identificação de problemas

7. **Script de diagnóstico**:
   - Adicionado script test-csrf.sh para ajudar a identificar problemas com CSRF
   - O script testa diversas configurações e exibe informações úteis para depuração

## Instruções para implantação

1. Faça backup dos arquivos modificados:
   ```bash
   cp config/wsgi.py config/wsgi.py.bak
   cp .env .env.bak
   cp docker-compose.yml docker-compose.yml.bak
   cp nginx.conf nginx.conf.bak
   cp config/settings.py config/settings.py.bak
   cp entrypoint.sh entrypoint.sh.bak
   ```

2. Aplique as alterações conforme descrito acima.

3. Torne o script de teste executável:
   ```bash
   chmod +x test-csrf.sh
   ```

4. Crie o diretório de logs para depuração CSRF:
   ```bash
   mkdir -p logs
   ```

5. Reconstrua e reinicie os contêineres Docker:
   ```bash
   docker-compose down
   docker-compose build web
   docker-compose up -d
   ```

6. Verifique os logs para identificar possíveis erros:
   ```bash
   docker-compose logs -f web
   ```

7. Execute o script de teste CSRF para verificar a configuração:
   ```bash
   ./test-csrf.sh gvd-system.com.br
   ```

8. Teste o acesso HTTPS ao sistema para confirmar que os problemas de CSRF foram resolvidos.

9. Verifique os logs específicos de CSRF:
   ```bash
   docker-compose exec web cat /app/logs/django-csrf.log
   ```

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