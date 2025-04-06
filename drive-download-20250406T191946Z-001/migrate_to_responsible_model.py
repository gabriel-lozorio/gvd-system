# migrate_to_responsible_model.py
# Salve este arquivo na raiz do seu projeto e execute:
# python migrate_to_responsible_model.py

import os
import django

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar modelos necessários (após o setup do Django)
from apps.accounts.models import Account
from apps.responsibles.models import Responsible

def migrate_responsible_data():
    """
    Cria registros no modelo Responsible a partir dos dados em responsible_name
    e atualiza os registros Account para referenciar os novos objetos Responsible
    """
    print("Iniciando migração de responsáveis...")
    
    # 1. Coletar nomes de responsáveis únicos
    responsibles_names = Account.objects.exclude(
        responsible_name__isnull=True
    ).exclude(
        responsible_name__exact=''
    ).values_list('responsible_name', flat=True).distinct()
    
    # 2. Criar registro de responsável para cada nome único
    responsible_map = {}  # Mapear nome -> objeto Responsible
    created_count = 0
    
    for name in responsibles_names:
        # Verificar se já existe um responsável com este nome
        responsible, created = Responsible.objects.get_or_create(
            name=name,
            defaults={
                'is_active': True,
            }
        )
        
        responsible_map[name] = responsible
        if created:
            created_count += 1
            print(f"Criado responsável: {name}")
    
    print(f"Criados {created_count} novos responsáveis.")
    
    # 3. Atualizar os registros de contas para apontar para os novos responsáveis
    updated_count = 0
    
    for account in Account.objects.exclude(responsible_name__isnull=True).exclude(responsible_name__exact=''):
        if account.responsible_name in responsible_map:
            account.related_responsible = responsible_map[account.responsible_name]
            account.save(update_fields=['related_responsible'])
            updated_count += 1
    
    print(f"Atualizados {updated_count} registros de contas.")

if __name__ == "__main__":
    migrate_responsible_data()