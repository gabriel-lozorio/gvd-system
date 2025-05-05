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
    iputils-ping \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project
COPY . .

# Copiar wsgi.py atualizado
RUN echo "import os\nfrom django.core.wsgi import get_wsgi_application\nos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')\napplication = get_wsgi_application()" > /app/config/wsgi.py

# Create directory for logs and static files
RUN mkdir -p /var/log/django /app/staticfiles /app/media

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Run as non-root user for better security
RUN useradd -m appuser
RUN chown -R appuser:appuser /app /var/log/django /app/staticfiles /app/media && \
    chmod -R 755 /var/log/django /app/staticfiles /app/media && \
    find /app -type d -exec chmod 755 {} \;

USER appuser

# Run entrypoint script
ENTRYPOINT ["/entrypoint.sh"]