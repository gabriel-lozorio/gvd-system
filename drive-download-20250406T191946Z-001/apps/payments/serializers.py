# apps/payments/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.payments.models import Payment, Receipt
from apps.accounts.models import Account


class PaymentSerializer(serializers.ModelSerializer):
    """Serializer para pagamentos"""
    account_description = serializers.CharField(source='account.description', read_only=True)
    
    class Meta:
        model = Payment
        fields = [
            'id', 'account', 'account_description', 'payment_date', 
            'payment_location', 'amount_paid', 'created_at', 'updated_at'
        ]
    
    def validate_account(self, account):
        """Validação da conta"""
        if account.type != Account.AccountType.PAYABLE:
            raise serializers.ValidationError(
                _("Pagamentos só podem ser registrados para contas a pagar")
            )
        return account


class ReceiptSerializer(serializers.ModelSerializer):
    """Serializer para recebimentos"""
    account_description = serializers.CharField(source='account.description', read_only=True)
    
    class Meta:
        model = Receipt
        fields = [
            'id', 'account', 'account_description', 'receipt_date',
            'receipt_location', 'amount_received', 'interest',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['interest']
    
    def validate_account(self, account):
        """Validação da conta"""
        if account.type != Account.AccountType.RECEIVABLE:
            raise serializers.ValidationError(
                _("Recebimentos só podem ser registrados para contas a receber")
            )
        return account