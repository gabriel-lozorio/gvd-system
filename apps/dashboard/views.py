# apps/dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import json
from decimal import Decimal
from datetime import datetime, date, timedelta

from django.core.serializers.json import DjangoJSONEncoder
from apps.accounts.models import Account
from apps.dashboard.services import DashboardService


@login_required
def dashboard(request):
    """
    Main dashboard view with pre-filtered summary data
    """
    today = timezone.now().date()
    
    # Default dates: first and last day of current month
    first_day = date(today.year, today.month, 1)
    if today.month == 12:
        last_day = date(today.year+1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(today.year, today.month+1, 1) - timedelta(days=1)
    
    # Próximas contas a pagar (próximos 30 dias)
    next_payable_accounts = Account.objects.filter(
        type=Account.AccountType.PAYABLE,
        status=Account.AccountStatus.OPEN,
        due_date__gte=today,
        due_date__lte=today + timedelta(days=30)
    ).select_related('category').order_by('due_date')[:5]
    
    # Próximas contas a receber (próximos 30 dias)
    next_receivable_accounts = Account.objects.filter(
        type=Account.AccountType.RECEIVABLE,
        status=Account.AccountStatus.OPEN,
        due_date__gte=today,
        due_date__lte=today + timedelta(days=30)
    ).order_by('due_date')[:5]
    
    # Dados para os gráficos - já filtrados por período
    initial_summary = DashboardService.get_date_range_summary(first_day, last_day)
    category_data = DashboardService.get_category_summary(today.year, today.month)
    evolution_data = DashboardService.get_monthly_evolution()
    
    dashboard_data = {
        'summary': initial_summary,
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
    
    # Prepare initial month name
    initial_month_name = datetime(today.year, today.month, 1).strftime('%B')
    
    context = {
        'next_payable_accounts': next_payable_accounts,
        'next_receivable_accounts': next_receivable_accounts,
        'dashboard_data': json.dumps(dashboard_data, cls=DjangoJSONEncoder),
        'start_date': first_day.strftime("%Y-%m-%d"),
        'end_date': last_day.strftime("%Y-%m-%d"),
        'initial_summary': initial_summary,
        'initial_month_name': initial_month_name,
        'current_year': today.year,
        'period': 'current'
    }
    
    return render(request, 'dashboard/index.html', context)


@login_required
def dashboard_summary_partial(request):
    """
    Dashboard summary view (htmx partial)
    Handles both period-based and date range filtering with default date values
    """
    period = request.GET.get('period', 'current')
    reset = request.GET.get('reset') == 'true'  # Check if reset parameter is present
    
    # Determine base period
    today = timezone.now().date()
    year = today.year
    month = today.month
    
    if period == 'last':
        # Previous month
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
    elif period == 'next':
        # Next month
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
    
    # Calculate first and last day of the selected month
    first_day = date(year, month, 1)
    if month == 12:
        last_day = date(year+1, 1, 1) - timedelta(days=1)
    else:
        last_day = date(year, month+1, 1) - timedelta(days=1)
    
    # Get filter dates if provided and not resetting, otherwise use defaults
    if not reset:
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date:
            start_date = datetime.strptime(start_date, "%Y-%m-%d").date()
        else:
            start_date = first_day
            
        if end_date:
            end_date = datetime.strptime(end_date, "%Y-%m-%d").date()
        else:
            end_date = last_day
    else:
        # When resetting, use the default dates (first and last day of month)
        start_date = first_day
        end_date = last_day
    
    # Use the dates for summary calculation
    summary_data = DashboardService.get_date_range_summary(start_date, end_date)
    
    # Display name based on date range
    if (start_date == first_day and end_date == last_day):
        month_name = datetime(year, month, 1).strftime('%B')
    else:
        month_name = f"{start_date.strftime('%d/%m/%Y')} a {end_date.strftime('%d/%m/%Y')}"
    
    context = {
        'summary': summary_data,
        'year': year,
        'month': month,
        'month_name': month_name,
        'period': period,
        'start_date': start_date.strftime("%Y-%m-%d"),
        'end_date': end_date.strftime("%Y-%m-%d")
    }
    
    return render(request, 'dashboard/partials/summary.html', context)