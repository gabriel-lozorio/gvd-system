# migrate_responsible_data.py
# Salve este arquivo na raiz do seu projeto e execute:
# python migrate_responsible_data.py

import os
import django

# Configurar ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Importar modelos necessários (após o setup do Django)
from apps.accounts.models import Account

def migrate_responsible_data():
    """
    Transfere nome do usuário responsável para o campo responsible_name
    """
    updated_count = 0
    
    # Transfere nome do usuário para o campo responsible_name
    for account in Account.objects.all():
        if account.responsible:
            if account.responsible.get_full_name():
                account.responsible_name = account.responsible.get_full_name()
            else:
                account.responsible_name = account.responsible.username
            account.save(update_fields=['responsible_name'])
            updated_count += 1
    
    print(f"Migrados {updated_count} registros.")

if __name__ == "__main__":
    migrate_responsible_data()