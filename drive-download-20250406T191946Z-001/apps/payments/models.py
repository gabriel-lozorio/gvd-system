# apps/payments/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.core.models import TimeStampedModel
from apps.accounts.models import Account
from django.core.exceptions import ValidationError


class Payment(TimeStampedModel):
    """
    Modelo para registrar pagamentos de contas a pagar
    """
    account = models.ForeignKey(
        Account,
        verbose_name=_("Conta"),
        on_delete=models.CASCADE,
        related_name="payments"
    )
    payment_date = models.DateField(_("Data de pagamento"))
    payment_location = models.CharField(_("Local de pagamento"), max_length=100)
    amount_paid = models.DecimalField(_("Valor pago"), max_digits=15, decimal_places=2)
    
    class Meta:
        verbose_name = _("Pagamento")
        verbose_name_plural = _("Pagamentos")
    
    def __str__(self):
        return f"Pagamento {self.account} - {self.payment_date}"
    
    def clean(self):
        """Validações adicionais"""
        if self.account.type != Account.AccountType.PAYABLE:
            raise ValidationError(_("Pagamentos só podem ser registrados para contas a pagar"))


class Receipt(TimeStampedModel):
    """
    Modelo para registrar recebimentos de contas a receber
    """
    account = models.ForeignKey(
        Account,
        verbose_name=_("Conta"),
        on_delete=models.CASCADE,
        related_name="receipts"
    )
    receipt_date = models.DateField(_("Data de recebimento"))
    receipt_location = models.CharField(_("Local de recebimento"), max_length=100)
    amount_received = models.DecimalField(_("Valor recebido"), max_digits=15, decimal_places=2)
    interest = models.DecimalField(_("Juros"), max_digits=15, decimal_places=2, default=0)
    
    class Meta:
        verbose_name = _("Recebimento")
        verbose_name_plural = _("Recebimentos")
    
    def __str__(self):
        return f"Recebimento {self.account} - {self.receipt_date}"
    
    def clean(self):
        """Validações adicionais"""
        if self.account.type != Account.AccountType.RECEIVABLE:
            raise ValidationError(_("Recebimentos só podem ser registrados para contas a receber"))


@receiver(post_save, sender=Payment)
def update_account_status_after_payment(sender, instance, created, **kwargs):
    """Atualiza o status da conta após um pagamento"""
    if created:
        account = instance.account
        total_paid = account.payments.aggregate(total=models.Sum('amount_paid'))['total'] or 0
        
        if total_paid >= account.original_amount:
            account.status = Account.AccountStatus.PAID
        elif total_paid > 0:
            account.status = Account.AccountStatus.PARTIALLY_PAID
        
        account.save()


@receiver(post_save, sender=Receipt)
def update_account_status_after_receipt(sender, instance, created, **kwargs):
    """Atualiza o status da conta após um recebimento"""
    if created:
        account = instance.account
        total_received = account.receipts.aggregate(
            total=models.Sum('amount_received')
        )['total'] or 0
        
        if total_received >= account.original_amount:
            account.status = Account.AccountStatus.PAID
        elif total_received > 0:
            account.status = Account.AccountStatus.PARTIALLY_PAID
        
        account.save()