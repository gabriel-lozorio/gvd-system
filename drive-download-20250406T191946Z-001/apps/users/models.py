# apps/users/models.py
from django.db import models
from django.contrib.auth.models import User


# Extender a classe User com método para obter iniciais
def get_initials(self):
    """
    Retorna as iniciais do nome e sobrenome do usuário
    """
    initials = ""
    if self.first_name:
        initials += self.first_name[0].upper()
    if self.last_name:
        initials += self.last_name[0].upper()
    if not initials:
        initials = self.username[0].upper()
    return initials

# Adiciona o método ao model User
User.add_to_class('get_initials', get_initials)