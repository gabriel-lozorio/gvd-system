# apps/payments/services.py
from datetime import datetime
from decimal import Decimal
from django.db import transaction
from django.utils import timezone

from apps.accounts.models import Account
from apps.payments.models import Payment, Receipt


class PaymentService:
    """
    Service for processing and managing payments for accounts payable.
    
    This service handles payment registration and validation.
    """
    
    @classmethod
    def _ensure_decimal(cls, value):
        """Garante que o valor é um Decimal, convertendo de string se necessário"""
        if isinstance(value, str):
            # Remove separadores de milhar e substitui vírgula por ponto
            value = value.replace('.', '').replace(',', '.')
        return Decimal(str(value))
    
    @classmethod
    @transaction.atomic
    def register_payment(cls, account_id, payment_date, payment_location, amount_paid):
        """
        Registers a payment for an account payable.
        
        Args:
            account_id (int): ID of the account being paid
            payment_date (date): Date when payment was made
            payment_location (str): Location or method of payment
            amount_paid (Decimal or str): Amount that was paid
            
        Returns:
            Payment: The created payment record
            
        Raises:
            ValueError: If account type is not PAYABLE
            Account.DoesNotExist: If account with given ID doesn't exist
        """
        account = Account.objects.get(id=account_id)
        
        # Garantir que amount_paid é um Decimal
        amount_paid = cls._ensure_decimal(amount_paid)
        
        if account.type != Account.AccountType.PAYABLE:
            raise ValueError("Payments can only be registered for accounts payable")
        
        if account.status == Account.AccountStatus.PAID:
            raise ValueError("This account has already been fully paid")
            
        if amount_paid <= 0:
            raise ValueError("Payment amount must be greater than zero")
        
        payment = Payment.objects.create(
            account=account,
            payment_date=payment_date,
            payment_location=payment_location,
            amount_paid=amount_paid
        )
        
        # Status update is handled by post_save signal
        
        return payment


class ReceiptService:
    """
    Serviço para processamento de recebimentos
    """
    
    # Taxa de juros padrão (2% ao dia)
    DEFAULT_INTEREST_RATE = Decimal('0.02')
    
    @classmethod
    def _ensure_decimal(cls, value):
        """Garante que o valor é um Decimal, convertendo de string se necessário"""
        if isinstance(value, str):
            # Remove separadores de milhar e substitui vírgula por ponto
            value = value.replace('.', '').replace(',', '.')
        return Decimal(str(value))
    
    @classmethod
    @transaction.atomic
    def register_receipt(cls, account_id, receipt_date, receipt_location, amount_received, interest_rate=None):
        """
        Registra um recebimento para uma conta a receber, incluindo cálculo de juros se estiver em atraso
        """
        account = Account.objects.get(id=account_id)
        
        # Garantir que amount_received é um Decimal
        amount_received = cls._ensure_decimal(amount_received)
        
        if account.type != Account.AccountType.RECEIVABLE:
            raise ValueError("Só é possível registrar recebimentos para contas a receber")
        
        # Calcula juros se estiver atrasado
        interest = Decimal('0')
        receipt_date_obj = datetime.strptime(receipt_date, "%Y-%m-%d").date() if isinstance(receipt_date, str) else receipt_date
        
        if receipt_date_obj > account.due_date:
            days_late = (receipt_date_obj - account.due_date).days
            rate = interest_rate if interest_rate is not None else cls.DEFAULT_INTEREST_RATE
            interest = account.original_amount * rate * days_late
        
        receipt = Receipt.objects.create(
            account=account,
            receipt_date=receipt_date,
            receipt_location=receipt_location,
            amount_received=amount_received,
            interest=interest
        )
        
        # A atualização do status é feita pelo signal post_save
        
        return receipt
    