# create_responsibles_table.py
import os
import django

# Configure o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.db import connection

def create_responsibles_table():
    with connection.cursor() as cursor:
        # Verificar se a tabela existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='responsibles_responsible'")
        table_exists = cursor.fetchone()
        
        if not table_exists:
            print("A tabela responsibles_responsible não existe. Criando...")
            # SQL para criar a tabela baseado na migração 0001_initial
            cursor.execute("""
            CREATE TABLE "responsibles_responsible" (
                "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                "created_at" datetime NOT NULL,
                "updated_at" datetime NOT NULL,
                "name" varchar(100) NOT NULL,
                "email" varchar(254) NULL,
                "phone" varchar(20) NULL,
                "notes" text NULL,
                "is_active" bool NOT NULL
            )
            """)
            print("Tabela criada com sucesso!")
        else:
            print("A tabela responsibles_responsible já existe.")

if __name__ == "__main__":
    create_responsibles_table()