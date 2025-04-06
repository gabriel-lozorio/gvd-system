# apps/accounts/tasks.py
from celery import shared_task
from django.utils import timezone
from apps.accounts.services import AccountService


@shared_task
def update_account_status():
    """
    Tarefa para atualizar o status das contas diariamente
    (Open -> Overdue para contas vencidas)
    """
    updated_count = AccountService.update_account_status()
    return f"Atualizadas {updated_count} contas para status 'Vencida'"


@shared_task
def generate_recurring_accounts(parent_account_id):
    """
    Tarefa para gerar contas recorrentes
    """
    from apps.accounts.models import Account
    
    try:
        parent_account = Account.objects.get(id=parent_account_id)
        AccountService._generate_recurring_installments(parent_account)
        return f"Geradas parcelas para conta {parent_account_id}"
    except Account.DoesNotExist:
        return f"Conta {parent_account_id} não encontrada"
    except Exception as e:
        return f"Erro ao gerar parcelas: {str(e)}"