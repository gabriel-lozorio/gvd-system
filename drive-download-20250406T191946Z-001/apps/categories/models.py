# apps/categories/models.py
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.models import TimeStampedModel


class Category(TimeStampedModel):
    """
    Modelo para categorias de contas
    """
    name = models.CharField(_("Nome"), max_length=100)
    description = models.TextField(_("Descrição"), blank=True)
    parent = models.ForeignKey(
        "self", 
        verbose_name=_("Categoria pai"),
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name="children"
    )

    class Meta:
        verbose_name = _("Categoria")
        verbose_name_plural = _("Categorias")
        ordering = ["name"]

    def __str__(self):
        return self.name
    
    @property
    def full_path(self):
        """Retorna o caminho completo da categoria (incluindo hierarquia)"""
        if self.parent:
            return f"{self.parent.full_path} > {self.name}"
        return self.name