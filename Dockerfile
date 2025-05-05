FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies in one layer to reduce image size
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

# Create necessary directories with proper permissions before copying app
RUN mkdir -p /app/staticfiles /app/media /var/log/django && \
    chmod 777 /app/staticfiles /app/media /var/log/django

# Create non-root user
RUN useradd -m appuser

# Copy project
COPY --chown=appuser:appuser . .

# Update wsgi.py
RUN echo "import os\nfrom django.core.wsgi import get_wsgi_application\nos.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')\napplication = get_wsgi_application()" > /app/config/wsgi.py

# Copy entrypoint script
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Final permission setup
RUN chown -R appuser:appuser /app /var/log/django /app/staticfiles /app/media && \
    find /app -type d -exec chmod 755 {} \;

# Switch to non-root user
USER appuser

# Run entrypoint script
ENTRYPOINT ["/entrypoint.sh"]