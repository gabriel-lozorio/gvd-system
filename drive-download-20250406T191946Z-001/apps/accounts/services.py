# apps/accounts/services.py
from datetime import datetime, timedelta
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Account


class AccountService:
    """
    Service class for account management operations.
    
    This service encapsulates business logic related to financial accounts,
    including creation, status updates, and recurring installment generation.
    """

    @classmethod
    def create_account(cls, data):
        """
        Creates a new account and generates installments if it's recurring.
        
        Args:
            data (dict): Account data including type, category, amounts, dates, etc.
            
        Returns:
            Account: The created account instance.
            
        Raises:
            ValueError: If validation fails (e.g., due date before issue date).
        """
        with transaction.atomic():
            # Additional validation
            if data['due_date'] < data['issue_date']:
                raise ValueError("Data de vencimento não pode ser anterior à data de emissão")
            
            # Create main account
            account = Account.objects.create(**data)
            
            # If recurring, create installments
            if account.is_recurring and account.installment_count:
                cls._generate_recurring_installments(account)
                
            return account
    
    @classmethod
    def _generate_recurring_installments(cls, parent_account):
        """
        Generates recurring installments automatically based on parent account.
        
        Args:
            parent_account (Account): The parent account with recurring settings.
        """
        # Já criamos a primeira parcela (a própria conta pai)
        for i in range(1, parent_account.installment_count):
            # Calcula a data de vencimento baseada na periodicidade
            if parent_account.periodicity_days:
                due_date = parent_account.due_date + timedelta(days=parent_account.periodicity_days * i)
            elif parent_account.specific_day_month:
                # Lógica para dia específico do mês
                due_date = parent_account.due_date.replace(day=1)  # Primeiro dia do mês
                due_date = (due_date + timedelta(days=32 * i)).replace(day=min(parent_account.specific_day_month, 28))
            else:
                # Se nenhuma periodicidade for definida, use mensal no mesmo dia
                next_month = parent_account.due_date.month + i
                next_year = parent_account.due_date.year + (next_month - 1) // 12
                next_month = ((next_month - 1) % 12) + 1
                due_date = parent_account.due_date.replace(year=next_year, month=next_month)
            
            # Cria a parcela filha com o novo campo responsible_name
            Account.objects.create(
                type=parent_account.type,
                category=parent_account.category,
                document_number=parent_account.document_number,
                responsible_name=parent_account.responsible_name,
                issue_date=parent_account.issue_date,
                due_date=due_date,
                description=f"{parent_account.description} - Parcela {i+1}/{parent_account.installment_count}" if parent_account.description else f"Parcela {i+1}/{parent_account.installment_count}",
                original_amount=parent_account.original_amount,
                status=Account.AccountStatus.OPEN,
                is_recurring=False,  # Parcelas não são recorrentes
                parent_installment=parent_account
            )
    
    @classmethod
    def update_account_status(cls):
        """
        Atualiza o status das contas baseado nas datas de vencimento
        """
        today = timezone.now().date()
        # Atualiza contas em aberto que venceram
        return Account.objects.filter(
            status=Account.AccountStatus.OPEN,
            due_date__lt=today
        ).update(status=Account.AccountStatus.OVERDUE)