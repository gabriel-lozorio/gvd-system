# apps/dashboard/services.py
from django.db.models import Sum, Count, Case, When, IntegerField, F, Value
from django.db.models.functions import TruncMonth
from django.utils import timezone
from collections import defaultdict
from datetime import date, timedelta

from apps.accounts.models import Account
from apps.payments.models import Payment, Receipt


class DashboardService:
    """
    Serviço para gerar dados do dashboard
    """
    
    @classmethod
    def get_monthly_summary(cls, year=None, month=None):
        """
        Obtém resumo mensal de contas a pagar e receber
        """
        today = timezone.now().date()
        year = year or today.year
        month = month or today.month
        
        # Contas a pagar do mês
        payables = Account.objects.filter(
            type=Account.AccountType.PAYABLE,
            due_date__year=year,
            due_date__month=month
        )
        
        # Contas a receber do mês
        receivables = Account.objects.filter(
            type=Account.AccountType.RECEIVABLE,
            due_date__year=year,
            due_date__month=month
        )
        
        # Total a pagar
        total_payable = payables.aggregate(total=Sum('original_amount'))['total'] or 0
        
        # Total a receber
        total_receivable = receivables.aggregate(total=Sum('original_amount'))['total'] or 0
        
        # Total pago
        total_paid = Payment.objects.filter(
            payment_date__year=year,
            payment_date__month=month
        ).aggregate(total=Sum('amount_paid'))['total'] or 0
        
        # Total recebido
        total_received = Receipt.objects.filter(
            receipt_date__year=year,
            receipt_date__month=month
        ).aggregate(total=Sum('amount_received'))['total'] or 0
        
        # Contas em atraso
        overdue_payables = payables.filter(
            status=Account.AccountStatus.OVERDUE
        ).count()
        
        overdue_receivables = receivables.filter(
            status=Account.AccountStatus.OVERDUE
        ).count()
        
        return {
            'total_payable': total_payable,
            'total_receivable': total_receivable,
            'total_paid': total_paid,
            'total_received': total_received,
            'overdue_payables': overdue_payables,
            'overdue_receivables': overdue_receivables,
            'projected_balance': total_receivable - total_payable,
            'actual_balance': total_received - total_paid
        }
    
    @classmethod
    def get_category_summary(cls, year=None, month=None):
        """
        Obtém resumo por categoria
        """
        today = timezone.now().date()
        year = year or today.year
        month = month or today.month
        
        # Contas por categoria
        payables_by_category = Account.objects.filter(
            type=Account.AccountType.PAYABLE,
            due_date__year=year,
            due_date__month=month
        ).values('category__name').annotate(
            total=Sum('original_amount')
        ).order_by('-total')
        
        receivables_by_category = Account.objects.filter(
            type=Account.AccountType.RECEIVABLE,
            due_date__year=year,
            due_date__month=month
        ).values('category__name').annotate(
            total=Sum('original_amount')
        ).order_by('-total')
        
        return {
            'payables_by_category': payables_by_category,
            'receivables_by_category': receivables_by_category
        }
    
    @classmethod
    def get_monthly_evolution(cls, months=6):
        """
        Obtém evolução mensal de receitas e despesas
        """
        today = timezone.now().date()
        
        # Últimos X meses
        start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        for i in range(months - 1):
            start_date = (start_date - timedelta(days=1)).replace(day=1)
        
        # Contas por mês
        payables_by_month = Account.objects.filter(
            type=Account.AccountType.PAYABLE,
            due_date__gte=start_date,
            due_date__lte=today
        ).annotate(
            month=TruncMonth('due_date')
        ).values('month').annotate(
            total=Sum('original_amount')
        ).order_by('month')
        
        receivables_by_month = Account.objects.filter(
            type=Account.AccountType.RECEIVABLE,
            due_date__gte=start_date,
            due_date__lte=today
        ).annotate(
            month=TruncMonth('due_date')
        ).values('month').annotate(
            total=Sum('original_amount')
        ).order_by('month')
        
        return {
            'payables_by_month': payables_by_month,
            'receivables_by_month': receivables_by_month
        }