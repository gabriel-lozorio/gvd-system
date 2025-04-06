# apps/core/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class TimeStampedModel(models.Model):
    """
    Base abstract model que fornece campos de created_at e updated_at
    """
    created_at = models.DateTimeField(_("Data de criação"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Data de atualização"), auto_now=True)

    class Meta:
        abstract = True




