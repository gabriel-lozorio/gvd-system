# Solução para problemas de CSRF no GVD System

Este documento fornece as correções aplicadas para resolver os problemas de verificação CSRF após a configuração do HTTPS e instruções para diagnosticar e resolver problemas relacionados.

## Problemas identificados

1. **Estrutura incorreta de configurações**: Tentativa de usar um módulo inexistente `config.settings.production`
2. **Erro no sistema de logging**: Tentativa de escrever em um diretório de log que não existia no container
3. **Configurações inadequadas de CSRF**: Configurações de segurança que não consideravam diferentes ambientes

## Soluções aplicadas

1. **Simplificação da estrutura de configurações**:
   - Revertido para usar o arquivo padrão `config.settings` em vez de tentar carregar um módulo inexistente
   - Todas as configurações relevantes foram adicionadas ao arquivo principal

2. **Correção do sistema de logging**:
   - Removido handler de arquivo que causava erros
   - Mantido apenas o logging para console para facilitar a depuração
   - Adicionado comando no entrypoint para criar o diretório de logs

3. **Configuração dinâmica baseada no ambiente**:
   - Configurações de segurança HTTPS são aplicadas apenas em produção
   - Em ambiente de desenvolvimento, as configurações são mais permissivas
   - Adicionados mais domínios à lista de CSRF_TRUSTED_ORIGINS

4. **Scripts de diagnóstico**:
   - debug-csrf.py: Exibe todas as configurações relevantes para CSRF
   - fix-csrf.sh: Script para reiniciar o sistema e verificar a configuração
   - test-csrf.sh: Script para testar especificamente a configuração de CSRF

## Como usar os scripts de diagnóstico

1. **Para verificar as configurações CSRF em execução**:
   ```bash
   docker-compose exec web python /app/debug-csrf.py
   ```

2. **Para reiniciar o sistema e verificar a configuração**:
   ```bash
   ./fix-csrf.sh
   ```

3. **Para testar a configuração CSRF com requisições reais**:
   ```bash
   ./test-csrf.sh gvd-system.com.br
   ```

## Ajustes em caso de problemas persistentes

Se você ainda enfrentar problemas de CSRF, tente estas soluções:

1. **Para ambiente de desenvolvimento**:
   - Edite o arquivo `.env` e defina `DEBUG=True`
   - Reinicie os contêineres com `docker-compose down && docker-compose up -d`

2. **Para ambiente de produção**:
   - Verifique se o Nginx está configurado corretamente para passar os cabeçalhos HTTP
   - Confirme que suas origens confiáveis incluem o protocolo correto (http:// ou https://)
   - Verifique se o domínio usado para acessar o site está na lista CSRF_TRUSTED_ORIGINS

3. **Se você estiver acessando através de um proxy ou load balancer**:
   - Certifique-se de que SECURE_PROXY_SSL_HEADER está configurado corretamente
   - Confirme que o proxy está enviando o cabeçalho HTTP_X_FORWARDED_PROTO

## Verificando logs para diagnóstico

```bash
# Verificar logs do contêiner web em tempo real
docker-compose logs -f web

# Verificar apenas mensagens de erro
docker-compose logs web | grep -i error

# Verificar especificamente mensagens relacionadas a CSRF
docker-compose logs web | grep -i csrf
```

Lembre-se de que o Django precisa estar configurado corretamente para lidar com HTTPS, especialmente quando está atrás de um proxy como o Nginx.