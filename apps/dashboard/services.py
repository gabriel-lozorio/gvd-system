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
        
        # Todas as contas a pagar do mês
        all_payables = Account.objects.filter(
            type=Account.AccountType.PAYABLE,
            due_date__year=year,
            due_date__month=month
        )

        # Apenas contas a pagar em aberto ou vencidas
        payables = all_payables.filter(
            status__in=[Account.AccountStatus.OPEN, Account.AccountStatus.OVERDUE]
        )

        # Todas as contas a receber do mês
        all_receivables = Account.objects.filter(
            type=Account.AccountType.RECEIVABLE,
            due_date__year=year,
            due_date__month=month
        )

        # Apenas contas a receber em aberto ou vencidas
        receivables = all_receivables.filter(
            status__in=[Account.AccountStatus.OPEN, Account.AccountStatus.OVERDUE]
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
        
        # Contas a pagar por categoria - incluindo todas para estatística completa
        payables_by_category = Account.objects.filter(
            type=Account.AccountType.PAYABLE,
            due_date__year=year,
            due_date__month=month
        ).values('category__name').annotate(
            total=Sum('original_amount')
        ).order_by('-total')

        # Contas a receber por categoria - incluindo todas para estatística completa
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
        Obtém evolução mensal de receitas e despesas - incluindo todas as contas para mostrar evolução histórica
        """
        today = timezone.now().date()

        # Últimos X meses
        start_date = (today.replace(day=1) - timedelta(days=1)).replace(day=1)
        for i in range(months - 1):
            start_date = (start_date - timedelta(days=1)).replace(day=1)

        # Gerar lista de meses para garantir que todos sejam incluídos
        month_list = []
        current_date = start_date
        while current_date <= today:
            month_list.append(current_date.replace(day=1))
            # Avançar para o próximo mês
            if current_date.month == 12:
                current_date = current_date.replace(year=current_date.year + 1, month=1)
            else:
                current_date = current_date.replace(month=current_date.month + 1)

        # Inclua TODAS as contas, independente do status, para mostrar a evolução histórica completa
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

        # Adicionar meses vazios para garantir continuidade do gráfico
        payables_dict = {item['month']: item['total'] for item in payables_by_month}
        receivables_dict = {item['month']: item['total'] for item in receivables_by_month}

        payables_result = []
        receivables_result = []

        for month in month_list:
            payables_result.append({
                'month': month,
                'total': payables_dict.get(month, 0)
            })
            receivables_result.append({
                'month': month,
                'total': receivables_dict.get(month, 0)
            })

        return {
            'payables_by_month': payables_result,
            'receivables_by_month': receivables_result
        }

    @classmethod
    def get_date_range_summary(cls, start_date, end_date):
        """
        Get financial summary for a specific date range
        
        Args:
            start_date (date): Start date for the range
            end_date (date): End date for the range
            
        Returns:
            dict: Financial summary data for the period
        """
        # All payable accounts in the period (for reference)
        all_payables = Account.objects.filter(
            type=Account.AccountType.PAYABLE,
            due_date__gte=start_date,
            due_date__lte=end_date
        )

        # Only OPEN or OVERDUE payable accounts (to be paid)
        payables = all_payables.filter(
            status__in=[Account.AccountStatus.OPEN, Account.AccountStatus.OVERDUE]
        )

        # All receivable accounts in the period (for reference)
        all_receivables = Account.objects.filter(
            type=Account.AccountType.RECEIVABLE,
            due_date__gte=start_date,
            due_date__lte=end_date
        )

        # Only OPEN or OVERDUE receivable accounts (to be received)
        receivables = all_receivables.filter(
            status__in=[Account.AccountStatus.OPEN, Account.AccountStatus.OVERDUE]
        )
        
        # Total to pay
        total_payable = payables.aggregate(total=Sum('original_amount'))['total'] or 0
        
        # Total to receive
        total_receivable = receivables.aggregate(total=Sum('original_amount'))['total'] or 0
        
        # Total paid in the period
        total_paid = Payment.objects.filter(
            payment_date__gte=start_date,
            payment_date__lte=end_date
        ).aggregate(total=Sum('amount_paid'))['total'] or 0
        
        # Total received in the period
        total_received = Receipt.objects.filter(
            receipt_date__gte=start_date,
            receipt_date__lte=end_date
        ).aggregate(total=Sum('amount_received'))['total'] or 0
        
        # Overdue accounts
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