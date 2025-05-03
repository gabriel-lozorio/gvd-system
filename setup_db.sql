CREATE DATABASE financeiro_gvd;
CREATE USER financeiro WITH PASSWORD '100%Glps';
ALTER ROLE financeiro SET client_encoding TO 'utf8';
ALTER ROLE financeiro SET timezone TO 'America/Sao_Paulo';
GRANT ALL PRIVILEGES ON DATABASE financeiro_gvd TO financeiro;