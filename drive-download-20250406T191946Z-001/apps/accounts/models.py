# apps/accounts/models.py

from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.core.models import TimeStampedModel

User = get_user_model()

class Account(TimeStampedModel):
    class AccountType(models.TextChoices):
        PAYABLE = "PAYABLE", _("A Pagar")
        RECEIVABLE = "RECEIVABLE", _("A Receber")
    
    class AccountStatus(models.TextChoices):
        OPEN = "OPEN", _("Em Aberto")
        PAID = "PAID", _("Paga")
        OVERDUE = "OVERDUE", _("Vencida")
        PARTIALLY_PAID = "PARTIALLY_PAID", _("Parcialmente Paga")
        CANCELED = "CANCELED", _("Cancelada")
    
    type = models.CharField(_("Tipo"), max_length=20, choices=AccountType.choices, db_index=True)
    category = models.ForeignKey('categories.Category', verbose_name=_("Categoria"), on_delete=models.PROTECT, related_name='accounts')
    document_number = models.CharField(_("Número do Documento"), max_length=50, blank=True)
    
    # Campos de responsável
    # Mantém o campo antigo para compatibilidade
    responsible = models.ForeignKey(
        User,
        verbose_name=_("Responsável (Antigo)"),
        on_delete=models.PROTECT,
        related_name='accounts',
        null=True,
        blank=True
    )
    
    # Campo texto (para retrocompatibilidade)
    responsible_name = models.CharField(_("Nome do Responsável"), max_length=100, blank=True, null=True)
    
    # Novo campo com relação para o modelo Responsible
    related_responsible = models.ForeignKey(
        'responsibles.Responsible',
        verbose_name=_("Responsável"),
        on_delete=models.PROTECT,
        related_name='related_accounts',
        null=True,
        blank=True
    )
    
    issue_date = models.DateField(_("Data de Emissão"), default=timezone.now)    
    due_date = models.DateField(_("Data de Vencimento"))
    description = models.CharField(_("Descrição"), max_length=255, blank=True)
    original_amount = models.DecimalField(_("Valor Original"), max_digits=15, decimal_places=2)
    status = models.CharField(_("Status"), max_length=20, choices=AccountStatus.choices, default=AccountStatus.OPEN, db_index=True)
    is_recurring = models.BooleanField(_("É Recorrente"), default=False)
    installment_count = models.IntegerField(_("Número de Parcelas"), null=True, blank=True)
    periodicity_days = models.IntegerField(_("Periodicidade (Dias)"), null=True, blank=True)
    specific_day_month = models.IntegerField(_("Dia Específico do Mês"), null=True, blank=True)
    parent_installment = models.ForeignKey('self', verbose_name=_("Parcela Pai"), on_delete=models.SET_NULL, null=True, blank=True, related_name='child_installments')

    class Meta:
        verbose_name = _("Conta")
        verbose_name_plural = _("Contas")
        ordering = ["due_date"]

    def __str__(self):
        return f"{self.get_type_display()} - {self.description or 'Sem descrição'}"
    
    def save(self, *args, **kwargs):
        # Se temos um related_responsible, garantimos que o responsible_name está sincronizado
        if self.related_responsible and (not self.responsible_name or 
                                         self.responsible_name != self.related_responsible.name):
            self.responsible_name = self.related_responsible.name
            
        super().save(*args, **kwargs)
    
    @property
    def is_overdue(self):
        """Check if the account is overdue."""
        return self.status == self.AccountStatus.OPEN and self.due_date < timezone.now().date()
    
    @property
    def days_overdue(self):
        """Calculate how many days the account is overdue."""
        if not self.is_overdue:
            return 0
        return (timezone.now().date() - self.due_date).days