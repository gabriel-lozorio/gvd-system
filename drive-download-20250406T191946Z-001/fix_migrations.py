# fix_migrations.py
import os
import django
from datetime import datetime

# Configure o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar o módulo de conexão
from django.db import connection

def fix_migration_history():
    with connection.cursor() as cursor:
        # Verificar o estado atual das migrações
        print("Estado atual das migrações:")
        cursor.execute("SELECT id, app, name, applied FROM django_migrations WHERE app IN ('accounts', 'responsibles') ORDER BY applied")
        migrations = cursor.fetchall()
        for migration in migrations:
            print(f"ID: {migration[0]}, App: {migration[1]}, Migration: {migration[2]}, Applied: {migration[3]}")
        
        print("\nCorrigindo o histórico de migrações...")
        
        # Verificar se a migração responsibles.0001_initial existe na tabela
        cursor.execute("SELECT COUNT(*) FROM django_migrations WHERE app='responsibles' AND name='0001_initial'")
        exists = cursor.fetchone()[0]
        
        if exists == 0:
            # Se não existe, insira a migração responsibles.0001_initial com uma data anterior
            # à accounts.0003_account_related_responsible_and_more
            cursor.execute("""
            INSERT INTO django_migrations (app, name, applied) 
            SELECT 'responsibles', '0001_initial', 
                (SELECT applied FROM django_migrations 
                WHERE app='accounts' AND name='0002_add_responsible_name_field')
            """)
            print("Adicionada migração responsibles.0001_initial")
        else:
            print("A migração responsibles.0001_initial já existe")
        
        # Verificar o novo estado das migrações
        print("\nNovo estado das migrações:")
        cursor.execute("SELECT id, app, name, applied FROM django_migrations WHERE app IN ('accounts', 'responsibles') ORDER BY applied")
        migrations = cursor.fetchall()
        for migration in migrations:
            print(f"ID: {migration[0]}, App: {migration[1]}, Migration: {migration[2]}, Applied: {migration[3]}")

if __name__ == "__main__":
    fix_migration_history()
    print("\nCorreção concluída. Tente executar 'python manage.py migrate' agora.")