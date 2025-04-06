# apps/reports/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def report_list(request):
    """
    View temporária para listagem de relatórios
    """
    context = {
        'title': 'Relatórios',
        'message': 'Módulo de relatórios em desenvolvimento.'
    }
    return render(request, 'reports/list.html', context)