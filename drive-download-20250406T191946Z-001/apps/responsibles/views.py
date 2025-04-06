# apps/responsibles/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from django.db.models import Q

from .models import Responsible
from .forms import ResponsibleForm


@login_required
def responsible_list(request):
    """
    Lista de responsáveis com filtro de pesquisa
    """
    search_query = request.GET.get('search', '')
    
    if search_query:
        responsibles = Responsible.objects.filter(
            Q(name__icontains=search_query) | 
            Q(email__icontains=search_query)
        )
    else:
        responsibles = Responsible.objects.all()
    
    # Por padrão, mostrar apenas ativos
    show_inactive = request.GET.get('show_inactive') == 'yes'
    if not show_inactive:
        responsibles = responsibles.filter(is_active=True)
    
    context = {
        'responsibles': responsibles,
        'search_query': search_query,
        'show_inactive': show_inactive
    }
    
    return render(request, 'responsibles/list.html', context)


@login_required
def responsible_create(request):
    """
    Criação de um novo responsável
    """
    if request.method == 'POST':
        form = ResponsibleForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, _("Responsável criado com sucesso!"))
            return redirect('responsible-list')
    else:
        form = ResponsibleForm()
    
    return render(request, 'responsibles/form.html', {
        'form': form,
        'is_creating': True
    })


@login_required
def responsible_detail(request, pk):
    """
    Detalhes do responsável
    """
    responsible = get_object_or_404(Responsible, pk=pk)
    
    # Contas relacionadas a este responsável
    from apps.accounts.models import Account
    accounts = Account.objects.filter(responsible_name=responsible.name)
    
    context = {
        'responsible': responsible,
        'accounts': accounts[:10],  # Limitar a 10 contas para performance
        'accounts_count': accounts.count()
    }
    
    return render(request, 'responsibles/detail.html', context)


@login_required
def responsible_update(request, pk):
    """
    Atualização de um responsável existente
    """
    responsible = get_object_or_404(Responsible, pk=pk)
    
    if request.method == 'POST':
        form = ResponsibleForm(request.POST, instance=responsible)
        if form.is_valid():
            form.save()
            messages.success(request, _("Responsável atualizado com sucesso!"))
            return redirect('responsible-list')
    else:
        form = ResponsibleForm(instance=responsible)
    
    return render(request, 'responsibles/form.html', {
        'form': form,
        'responsible': responsible,
        'is_creating': False
    })


@login_required
def responsible_toggle_status(request, pk):
    """
    Ativa/desativa um responsável
    """
    responsible = get_object_or_404(Responsible, pk=pk)
    responsible.is_active = not responsible.is_active
    responsible.save()
    
    status_msg = "ativado" if responsible.is_active else "desativado"
    messages.success(
        request, 
        _(f"Responsável {responsible.name} {status_msg} com sucesso!")
    )
    
    return redirect('responsible-list')