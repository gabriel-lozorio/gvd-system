# apps/dashboard/tasks.py
from celery import shared_task
from datetime import datetime, timezone
import csv
import os
from django.conf import settings

from apps.dashboard.services import DashboardService


@shared_task
def generate_monthly_report():
    """
    Celery task to generate a monthly financial report in CSV format.
    
    This task:
    1. Gets financial data for the previous month
    2. Creates a CSV file with summaries of payables/receivables
    3. Stores the report in the reports directory
    
    Returns:
        str: A message indicating the result of the operation
    """
    today = datetime.now()
    if today.month == 1:
        month = 12
        year = today.year - 1
    else:
        month = today.month - 1
        year = today.year
    
    # Obtém dados do mês anterior
    summary = DashboardService.get_monthly_summary(year, month)
    categories = DashboardService.get_category_summary(year, month)
    
    # Define o caminho para o diretório de relatórios
    reports_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Define o nome do arquivo
    filename = f"relatorio_financeiro_{year}_{month:02d}.csv"
    filepath = os.path.join(reports_dir, filename)
    
    # Escreve o relatório em CSV
    with open(filepath, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        
        # Cabeçalho
        writer.writerow(['Relatório Financeiro', f"{month:02d}/{year}"])
        writer.writerow([])
        
        # Resumo
        writer.writerow(['Resumo Financeiro'])
        writer.writerow(['Total a Pagar', summary['total_payable']])
        writer.writerow(['Total a Receber', summary['total_receivable']])
        writer.writerow(['Total Pago', summary['total_paid']])
        writer.writerow(['Total Recebido', summary['total_received']])
        writer.writerow(['Saldo Projetado', summary['projected_balance']])
        writer.writerow(['Saldo Real', summary['actual_balance']])
        writer.writerow(['Contas a Pagar em Atraso', summary['overdue_payables']])
        writer.writerow(['Contas a Receber em Atraso', summary['overdue_receivables']])
        writer.writerow([])
        
        # Contas por categoria
        writer.writerow(['Despesas por Categoria'])
        writer.writerow(['Categoria', 'Valor'])
        for category in categories['payables_by_category']:
            writer.writerow([category['category__name'], category['total']])
        
        writer.writerow([])
        writer.writerow(['Receitas por Categoria'])
        writer.writerow(['Categoria', 'Valor'])
        for category in categories['receivables_by_category']:
            writer.writerow([category['category__name'], category['total']])
    
    return f"Relatório mensal gerado: {filename}"


@shared_task
def send_overdue_notifications():
    """
    Envia notificações para contas vencidas
    """
    from apps.accounts.models import Account
    from django.core.mail import send_mail
    from django.conf import settings
    
    # Busca contas vencidas recentemente (último dia)
    yesterday = timezone.now().date() - timezone.timedelta(days=1)
    
    newly_overdue = Account.objects.filter(
        status=Account.AccountStatus.OVERDUE,
        due_date=yesterday
    ).select_related('responsible')
    
    # Agrupa por responsável
    by_responsible = {}
    for account in newly_overdue:
        if account.responsible.email not in by_responsible:
            by_responsible[account.responsible.email] = []
        by_responsible[account.responsible.email].append(account)
    
    # Envia email para cada responsável
    for email, accounts in by_responsible.items():
        accounts_text = "\n".join([
            f"- {account.description}: R$ {account.original_amount} (vencida em {account.due_date})"
            for account in accounts
        ])
        
        send_mail(
            subject='[Sistema Financeiro] Contas vencidas',
            message=f"""Olá,

Você tem {len(accounts)} contas vencidas no sistema financeiro:

{accounts_text}

Por favor, acesse o sistema para regularizar essas contas.

Atenciosamente,
Sistema Financeiro
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )
    
    return f"Enviadas notificações para {len(by_responsible)} responsáveis"