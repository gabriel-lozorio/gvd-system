# apps/responsibles/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Responsible(TimeStampedModel):
    """
    Modelo para responsáveis de contas
    """
    name = models.CharField(_("Nome"), max_length=100)
    email = models.EmailField(_("Email"), blank=True, null=True)
    phone = models.CharField(_("Telefone"), max_length=20, blank=True, null=True)
    notes = models.TextField(_("Observações"), blank=True, null=True)
    is_active = models.BooleanField(_("Ativo"), default=True)

    class Meta:
        verbose_name = _("Responsável")
        verbose_name_plural = _("Responsáveis")
        ordering = ["name"]

    def __str__(self):
        return self.name