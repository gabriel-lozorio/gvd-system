# apps/payments/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _
from decimal import Decimal

from apps.payments.models import Payment, Receipt


class DecimalBrField(forms.DecimalField):
    """Campo decimal que aceita entrada formatada com vírgula"""
    
    def to_python(self, value):
        """Converte o valor inserido pelo usuário para o formato interno"""
        if value in self.empty_values:
            return None
        
        # Substitui vírgula por ponto para processamento
        if isinstance(value, str):
            value = value.replace('.', '').replace(',', '.')
        
        return super().to_python(value)


class DecimalBrWidget(forms.TextInput):
    """Widget para exibir valores decimais no formato brasileiro"""
    
    def format_value(self, value):
        """Formata o valor para exibição (com vírgula)"""
        if value is None or value == '':
            return ''
        # Converte para decimal caso seja string
        if isinstance(value, str):
            try:
                value = Decimal(value.replace(',', '.'))
            except:
                return value
        # Formata com duas casas decimais e vírgula
        return str(value).replace('.', ',')


class PaymentForm(forms.ModelForm):
    """
    Formulário para registrar pagamentos
    """
    amount_paid = DecimalBrField(
        label=_("Valor Pago"),
        max_digits=15,
        decimal_places=2,
        widget=DecimalBrWidget(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Payment
        fields = ['payment_date', 'payment_location', 'amount_paid']
        widgets = {
            'payment_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_location': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ReceiptForm(forms.ModelForm):
    """
    Formulário para registrar recebimentos
    """
    amount_received = DecimalBrField(
        label=_("Valor Recebido"),
        max_digits=15,
        decimal_places=2,
        widget=DecimalBrWidget(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Receipt
        fields = ['receipt_date', 'receipt_location', 'amount_received']
        widgets = {
            'receipt_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'receipt_location': forms.TextInput(attrs={'class': 'form-control'}),
        }