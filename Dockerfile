FROM python:3.11-alpine

WORKDIR /app

# Instalar dependências
RUN apk update && apk upgrade && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    curl \
    wget

# Copiar requirements primeiro (para melhor uso de cache)
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# CORREÇÃO CRÍTICA: Copiar TODOS os arquivos para /app
COPY . /app/

# Garantir permissões de execução para o entrypoint
RUN chmod +x /app/entrypoint.sh

# Configuração de ambiente
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Expor porta da aplicação
EXPOSE 8000

# Executar entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "config.wsgi:application"]