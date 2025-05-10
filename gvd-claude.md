1. Para acessar o banco PostgreSQL com pgAdmin:

  O banco está hospedado em um contêiner Docker. Para acessá-lo com o pgAdmin:

  1. Exponha a porta do PostgreSQL - Adicione ao serviço db no docker-compose.yml:
  ports:
    - "5432:5432"
  2. Reconstrua os serviços:
  docker-compose down
  docker-compose up -d
  3. Conecte pelo pgAdmin usando:
    - Host: IP público da instância AWS
    - Porta: 5432
    - Usuário: financeiro (do DB_USER)
    - Senha: 1eD0hdZz5Lbi (do DB_PASSWORD)
    - Banco: financeiro_gvd (do DB_DB)

● Update Todos
  ⎿  ☒ Corrigir comando para remover imagens Docker
     ☒ Verificar arquivos de configuração do banco de dados
     ☒ Explicar localização e acesso ao banco PostgreSQL
     ☒ Reiniciar serviços com docker-compose
     ☒ Executar migrações do Django
     ☐ Explicar configuração HTTPS com domínio personalizado

● 2. Para configurar HTTPS com domínio personalizado:
  3. Compre um domínio e aponte para o IP da instância AWS criando um registro A
  4. Modifique o arquivo .env:
  ALLOWED_HOSTS=seu-dominio.com,www.seu-dominio.com,localhost,127.0.0.1
  5. Instale Certbot na instância:
  sudo apt update
  sudo apt install certbot python3-certbot-nginx
  6. Obtenha certificado SSL:
  sudo certbot --nginx -d seu-dominio.com -d www.seu-dominio.com
  7. Atualize o nginx.conf para suportar HTTPS:
  server {
      listen 80;
      server_name seu-dominio.com www.seu-dominio.com;
      return 301 https://$host$request_uri;
  }

  server {
      listen 443 ssl;
      server_name seu-dominio.com www.seu-dominio.com;

      ssl_certificate /etc/letsencrypt/live/seu-dominio.com/fullchain.pem;
      ssl_certificate_key /etc/letsencrypt/live/seu-dominio.com/privkey.pem;

      # Resto da configuração igual
      client_max_body_size 10M;

      location / {
          proxy_pass http://web:8000;
          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;
      }

      location /static/ {
          alias /var/www/html/static/;
      }

      location /media/ {
          alias /var/www/html/media/;
      }
  }
  8. Modifique docker-compose.yml para mapear a porta 443:
  nginx:
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/conf.d/default.conf
      - /etc/letsencrypt:/etc/letsencrypt
  9. Reinicie os serviços:
  docker-compose down
  docker-compose up -d
