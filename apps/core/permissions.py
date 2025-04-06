# apps/core/permissions.py
from rest_framework import permissions


class IsOwnerOrStaff(permissions.BasePermission):
    """
    Permissão personalizada que só permite acesso ao dono de um objeto ou a um staff.
    """
    def has_object_permission(self, request, view, obj):
        # Staff pode acessar qualquer objeto
        if request.user.is_staff:
            return True
        
        # Checa se o usuário é responsável/dono do objeto
        if hasattr(obj, 'responsible'):
            return obj.responsible == request.user
        elif hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        # Se não encontrar o atributo, nega o acesso
        return False