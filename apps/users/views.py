# apps/users/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _

from .forms import UserRegisterForm, UserUpdateForm


def register(request):
    """
    View para registro de novos usuários (temporariamente desativada)
    """
    # Funcionalidade de registro temporariamente desativada
    messages.info(request, _("Criação de novas contas temporariamente indisponível. Entre em contato com o administrador."))
    return redirect('login')

    # O código abaixo está temporariamente desativado
    """
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Conta criada com sucesso! Agora você pode fazer login."))
            return redirect('login')
    else:
        form = UserRegisterForm()

    return render(request, 'users/register.html', {'form': form})
    """


@login_required
def profile(request):
    """
    View para exibição e edição do perfil do usuário
    """
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, _("Seu perfil foi atualizado com sucesso!"))
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user)
    
    return render(request, 'users/profile.html', {'form': form})