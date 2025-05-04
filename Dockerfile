FROM python:3.11-alpine AS builder
WORKDIR /app

# Install build dependencies
RUN apk update && apk upgrade && apk add --no-cache \
    gcc \
    musl-dev \
    postgresql-client \
    postgresql-dev \
    jpeg-dev \
    zlib-dev \
    curl \
    wget

# Copy and install requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --prefix=/install

# Final stage
FROM python:3.11-alpine
WORKDIR /app

# Install runtime dependencies
RUN apk update && apk upgrade && apk add --no-cache \
    postgresql-client \
    wget \
    curl \
    jpeg \
    libpq

# Create required directories
RUN mkdir -p /app/staticfiles /app/media /var/log/django && \
    chmod 777 /var/log/django

# Copy dependencies from builder stage
COPY --from=builder /install /usr/local

# Copy application code
COPY . /app/

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Ensure scripts are executable
COPY entrypoint.sh /app/
RUN chmod +x /app/entrypoint.sh && \
    sed -i 's/\r$//' /app/entrypoint.sh

# Expose port
EXPOSE 8000

# Entrypoint
ENTRYPOINT ["/app/entrypoint.sh"]

# Run command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "config.wsgi:application"]