# apps/accounts/views.py (parcial - apenas funções principais)
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

# Aplicações locais
from apps.accounts.models import Account
from apps.accounts.forms import AccountForm
from apps.accounts.services import AccountService
from apps.categories.models import Category
from apps.payments.forms import PaymentForm, ReceiptForm
from apps.payments.services import PaymentService, ReceiptService

@login_required
def account_list(request):
    """
    Visualização de lista de contas com filtros e paginação
    """
    accounts = Account.objects.all().select_related('category')
    
    # Aplicar filtros
    account_type = request.GET.get('type')
    if account_type:
        accounts = accounts.filter(type=account_type)
    
    category_id = request.GET.get('category')
    if category_id:
        accounts = accounts.filter(category_id=category_id)
    
    status = request.GET.get('status')
    if status:
        accounts = accounts.filter(status=status)
    
    due_date_start = request.GET.get('due_date_start')
    if due_date_start:
        accounts = accounts.filter(due_date__gte=due_date_start)
    
    due_date_end = request.GET.get('due_date_end')
    if due_date_end:
        accounts = accounts.filter(due_date__lte=due_date_end)
    
    responsible_name = request.GET.get('responsible_name')
    if responsible_name:
        accounts = accounts.filter(responsible_name__icontains=responsible_name)
    
    search = request.GET.get('search')
    if search:
        accounts = accounts.filter(
            Q(description__icontains=search) |
            Q(document_number__icontains=search)
        )
    
    # Ordenação
    ordering = request.GET.get('ordering', 'due_date')
    accounts = accounts.order_by(ordering)
    
    # Paginação
    paginator = Paginator(accounts, 25)  # 25 contas por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Dados para filtros
    categories = Category.objects.all()
    responsibles = Account.objects.exclude(responsible_name__isnull=True).exclude(responsible_name='').values_list('responsible_name', flat=True).distinct()
    
    context = {
        'accounts': page_obj,
        'account_type': account_type,
        'categories': categories,
        'responsibles': responsibles,
        'ordering': ordering,
    }
    
    return render(request, 'accounts/list.html', context)


@login_required
def account_detail(request, pk):
    """
    Visualização de detalhes de uma conta
    """
    account = get_object_or_404(
        Account.objects.select_related('category', 'parent_installment'),
        pk=pk
    )
    
    # Obter pagamentos ou recebimentos relacionados
    if account.type == Account.AccountType.PAYABLE:
        transactions = account.payments.all().order_by('-payment_date')
    else:
        transactions = account.receipts.all().order_by('-receipt_date')
    
    # Obter parcelas filhas se for uma conta recorrente
    if account.is_recurring:
        child_installments = account.child_installments.all().order_by('due_date')
    else:
        child_installments = None
    
    context = {
        'account': account,
        'transactions': transactions,
        'child_installments': child_installments,
    }
    
    return render(request, 'accounts/detail.html', context)


@login_required
def account_create(request):
    """
    Criação de uma nova conta
    """
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            try:
                # Usar o serviço para criar a conta (e possíveis parcelas recorrentes)
                account = AccountService.create_account(form.cleaned_data)
                messages.success(request, _("Conta criada com sucesso!"))
                return redirect('account-detail', pk=account.id)
            except Exception as e:
                messages.error(request, str(e))
    else:
        # Pré-selecionar o tipo se fornecido via query parameter
        initial = {}
        account_type = request.GET.get('type')
        if account_type in [Account.AccountType.PAYABLE, Account.AccountType.RECEIVABLE]:
            initial['type'] = account_type
        
        form = AccountForm(initial=initial)
    
    context = {
        'form': form,
        'is_creating': True,
    }
    
    return render(request, 'accounts/form.html', context)


@login_required
def account_update(request, pk):
    """
    Atualização de uma conta existente
    """
    account = get_object_or_404(Account, pk=pk)
    
    # Verificar se a conta já foi paga ou recebida
    if account.status == Account.AccountStatus.PAID:
        messages.warning(request, _("Não é possível editar uma conta já paga."))
        return redirect('account-detail', pk=account.id)
    
    if request.method == 'POST':
        form = AccountForm(request.POST, instance=account)
        if form.is_valid():
            form.save()
            messages.success(request, _("Conta atualizada com sucesso!"))
            return redirect('account-detail', pk=account.id)
    else:
        form = AccountForm(instance=account)
    
    context = {
        'form': form,
        'account': account,
        'is_creating': False,
    }
    
    return render(request, 'accounts/form.html', context)

# Adicione estas funções ao arquivo apps/accounts/views.py

@login_required
def account_payment_form(request, pk):
    """
    Formulário para registrar pagamento (htmx partial)
    """
    account = get_object_or_404(Account, pk=pk)
    
    if account.type != Account.AccountType.PAYABLE:
        return HttpResponse("Tipo de conta inválido", status=400)
    
    today = timezone.now().date()
    
    context = {
        'account': account,
        'today': today,
    }
    
    return render(request, 'accounts/payment_form_modal.html', context)


@login_required
def account_receipt_form(request, pk):
    """
    Formulário para registrar recebimento (htmx partial)
    """
    account = get_object_or_404(Account, pk=pk)
    
    if account.type != Account.AccountType.RECEIVABLE:
        return HttpResponse("Tipo de conta inválido", status=400)
    
    today = timezone.now().date()
    
    context = {
        'account': account,
        'today': today,
    }
    
    return render(request, 'accounts/receipt_form_modal.html', context)


@login_required
@require_POST
def account_register_payment(request, pk):
    """
    Registrar um pagamento
    """
    from django.urls import reverse

    account = get_object_or_404(Account, pk=pk)

    if account.type != Account.AccountType.PAYABLE:
        messages.error(request, _("Só é possível registrar pagamentos para contas a pagar"))
        return redirect('account-detail', pk=account.id)

    form = PaymentForm(request.POST)
    form.instance.account = account  # Adiciona a conta ao formulário
    if form.is_valid():
        try:
            payment = PaymentService.register_payment(
                account_id=account.id,
                payment_date=form.cleaned_data['payment_date'],
                payment_location=form.cleaned_data['payment_location'],
                amount_paid=form.cleaned_data['amount_paid']
            )

            # Verifica se a requisição foi feita via HTMX
            if request.headers.get('HX-Request'):
                # Retorna uma mensagem simples de sucesso
                html = f'''
                <div id="payment-success-message" class="alert alert-success mt-2 mb-3" style="position: fixed; top: 20%; left: 50%; transform: translateX(-50%); z-index: 9999; min-width: 300px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <strong>Conta paga com sucesso!</strong>
                </div>
                <script>
                    // Remove o modal se estiver aberto
                    var modal = document.getElementById('payment-modal');
                    if (modal) {{
                        var bsModal = bootstrap.Modal.getInstance(modal);
                        if (bsModal) bsModal.hide();
                    }}

                    // Exibe a mensagem por 1.5 segundos, garantindo que seja visível
                    document.body.appendChild(document.getElementById('payment-success-message'));

                    // Atualiza a página após 1.5 segundos para mostrar o novo status
                    setTimeout(function() {{
                        window.location.reload();
                    }}, 1500);
                </script>
                '''
                return HttpResponse(html)

            messages.success(request, _("Pagamento registrado com sucesso!"))

        except Exception as e:
            messages.error(request, str(e))
            if request.headers.get('HX-Request'):
                return HttpResponse(f'<div class="alert alert-danger">{str(e)}</div>')
    else:
        error_msg = _("Erro ao registrar pagamento: ") + str(form.errors)
        messages.error(request, error_msg)
        if request.headers.get('HX-Request'):
            return HttpResponse(f'<div class="alert alert-danger">{error_msg}</div>')

    return redirect('account-detail', pk=account.id)


@login_required
@require_POST
def account_register_receipt(request, pk):
    """
    Registrar um recebimento
    """
    from django.urls import reverse

    account = get_object_or_404(Account, pk=pk)

    if account.type != Account.AccountType.RECEIVABLE:
        messages.error(request, _("Só é possível registrar recebimentos para contas a receber"))
        return redirect('account-detail', pk=account.id)

    form = ReceiptForm(request.POST)
    form.instance.account = account  # Adiciona a conta ao formulário
    if form.is_valid():
        try:
            receipt = ReceiptService.register_receipt(
                account_id=account.id,
                receipt_date=form.cleaned_data['receipt_date'],
                receipt_location=form.cleaned_data['receipt_location'],
                amount_received=form.cleaned_data['amount_received']
            )
            # Verifica se a requisição foi feita via HTMX
            if request.headers.get('HX-Request'):
                # Retorna uma div com mensagem de sucesso estilizada
                html = f'''
                <div id="receipt-success-message" class="alert alert-success mt-2 mb-3" style="position: fixed; top: 20%; left: 50%; transform: translateX(-50%); z-index: 9999; min-width: 300px; text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
                    <strong>Conta recebida com sucesso!</strong>
                </div>
                <script>
                    // Remove o modal se estiver aberto
                    var modal = document.getElementById('receipt-modal');
                    if (modal) {{
                        var bsModal = bootstrap.Modal.getInstance(modal);
                        if (bsModal) bsModal.hide();
                    }}

                    // Exibe a mensagem por 1.5 segundos, garantindo que seja visível
                    document.body.appendChild(document.getElementById('receipt-success-message'));

                    // Atualiza a página após 1.5 segundos para mostrar o novo status
                    setTimeout(function() {{
                        window.location.reload();
                    }}, 1500);
                </script>
                '''
                return HttpResponse(html)

            messages.success(request, _("Recebimento registrado com sucesso!"))
        except Exception as e:
            messages.error(request, str(e))
            if request.headers.get('HX-Request'):
                return HttpResponse(f'<div class="alert alert-danger">{str(e)}</div>')
    else:
        error_msg = _("Erro ao registrar recebimento: ") + str(form.errors)
        messages.error(request, error_msg)
        if request.headers.get('HX-Request'):
            return HttpResponse(f'<div class="alert alert-danger">{error_msg}</div>')

    return redirect('account-detail', pk=account.id)