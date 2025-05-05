FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . .

RUN mkdir -p /app/staticfiles /app/media \
    && chmod -R 777 /app/staticfiles /app/media \
    && find /app -type d -exec chmod 755 {} \;

# Copiar wsgi.py atualizado
RUN echo "import os\nfrom django.core.wsgi import get_wsgi_application\nos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')\napplication = get_wsgi_application()" > /app/config/wsgi.py

# Create directory for logs
RUN mkdir -p /var/log/django && chmod 777 /var/log/django

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    netcat-traditional \
    iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    
# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run as non-root user for better security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app /var/log/django
USER appuser

# Run entrypoint script
ENTRYPOINT ["/entrypoint.sh"]