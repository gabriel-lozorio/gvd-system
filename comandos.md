# Comandos Importantes para Django

Este documento reúne alguns dos comandos mais utilizados durante o desenvolvimento com Django, tanto em ambientes Windows quanto Linux. Lembre-se de que, dependendo da configuração do seu sistema, você pode precisar usar "python" ou "python3".

## Windows

### Ativar o Ambiente Virtual
Utilize o comando:
    .\venv\Scripts\activate

### Criar Superuser
Utilize o comando:
    python manage.py createsuperuser

### Abrir o Shell do Django (para operações manuais, como apagar dados de produção)
Utilize o comando:
    python manage.py shell

### Fazer Migrações (gerar as migrações a partir das alterações dos modelos)
Utilize o comando:
    python manage.py makemigrations

### Aplicar Migrações (atualizar o banco de dados)
Utilize o comando:
    python manage.py migrate

### Rodar o Servidor de Desenvolvimento
Utilize o comando:
    python manage.py runserver

### Coletar Arquivos Estáticos (usado principalmente em produção)
Utilize o comando:
    python manage.py collectstatic

### Criar um Novo App Django
Utilize o comando:
    python manage.py startapp nome_do_app

## Linux

### Ativar o Ambiente Virtual
Utilize o comando:
    source venv/bin/activate

### Criar Superuser
Utilize o comando:
    python3 manage.py createsuperuser

### Abrir o Shell do Django
Utilize o comando:
    python3 manage.py shell

### Fazer Migrações (gerar as migrações)
Utilize o comando:
    python3 manage.py makemigrations

### Aplicar Migrações (atualizar o banco de dados)
Utilize o comando:
    python3 manage.py migrate

### Rodar o Servidor de Desenvolvimento
Utilize o comando:
    python3 manage.py runserver

### Coletar Arquivos Estáticos (usado em produção)
Utilize o comando:
    python3 manage.py collectstatic

### Criar um Novo App Django
Utilize o comando:
    python3 manage.py startapp nome_do_app

## Notas Adicionais

- Ambiente Virtual:
  No Windows, utilize ".\venv\Scripts\activate"; no Linux, utilize "source venv/bin/activate".
- Python vs Python3:
  Dependendo da configuração do seu sistema, o comando para invocar o Python pode ser "python" ou "python3".
- Servidor de Desenvolvimento:
  O comando runserver inicia um servidor local para testes. Não o utilize em ambientes de produção.
- Migrations:
  Sempre que alterar seus modelos, utilize makemigrations para gerar as migrações e migrate para aplicá-las no banco de dados.
- Coletar Arquivos Estáticos:
  O comando collectstatic é fundamental para preparar os arquivos estáticos para um ambiente de produção.
