# apps/dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
import json

from apps.accounts.models import Account
from apps.dashboard.services import DashboardService


@login_required
def dashboard(request):
    """
    Dashboard principal
    """
    today = timezone.now().date()
    
    # Próximas contas a pagar (próximos 30 dias)
    next_payable_accounts = Account.objects.filter(
        type=Account.AccountType.PAYABLE,
        status=Account.AccountStatus.OPEN,
        due_date__gte=today,
        due_date__lte=today + timedelta(days=30)
    ).order_by('due_date')[:5]
    
    # Próximas contas a receber (próximos 30 dias)
    next_receivable_accounts = Account.objects.filter(
        type=Account.AccountType.RECEIVABLE,
        status=Account.AccountStatus.OPEN,
        due_date__gte=today,
        due_date__lte=today + timedelta(days=30)
    ).order_by('due_date')[:5]
    
    # Dados para os gráficos
    summary_data = DashboardService.get_monthly_summary()
    category_data = DashboardService.get_category_summary()
    evolution_data = DashboardService.get_monthly_evolution()
    
    # Preparar dados para os gráficos no formato JSON
    dashboard_data = {
        'summary': summary_data,
        'categories': {
            'payables': [
                {'category': item['category__name'], 'total': float(item['total'])}
                for item in category_data['payables_by_category']
            ],
            'receivables': [
                {'category': item['category__name'], 'total': float(item['total'])}
                for item in category_data['receivables_by_category']
            ]
        },
        'evolution': {
            'months': [item['month'].strftime('%b/%Y') for item in evolution_data['payables_by_month']],
            'payables': [float(item['total']) for item in evolution_data['payables_by_month']],
            'receivables': [float(item['total']) for item in evolution_data['receivables_by_month']]
        }
    }
    
    context = {
        'next_payable_accounts': next_payable_accounts,
        'next_receivable_accounts': next_receivable_accounts,
        'dashboard_data': json.dumps(dashboard_data)
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
def dashboard_summary_partial(request):
    """
    Resumo do dashboard (htmx partial)
    """
    period = request.GET.get('period', 'current')
    
    today = timezone.now().date()
    year = today.year
    month = today.month
    
    if period == 'last':
        # Mês anterior
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
    elif period == 'next':
        # Próximo mês
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    
    summary_data = DashboardService.get_monthly_summary(year, month)
    
    context = {
        'summary': summary_data,
        'year': year,
        'month': month,
        'month_name': datetime(year, month, 1).strftime('%B'),
        'period': period
    }
    
    return render(request, 'dashboard/partials/summary.html', context)