# apps/accounts/forms.py (atualizado)
from django import forms
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from decimal import Decimal, InvalidOperation

from apps.accounts.models import Account
from apps.categories.models import Category
from apps.responsibles.models import Responsible


class BrazilianDecimalField(forms.DecimalField):
    """Campo decimal customizado que aceita vírgula como separador decimal"""
    
    def to_python(self, value):
        """Converte a entrada do usuário para um valor Python (Decimal)"""
        if value in self.empty_values:
            return None
            
        if isinstance(value, str):
            # Remove pontos (separadores de milhar) e substitui vírgula por ponto
            value = value.replace('.', '').replace(',', '.')
        
        try:
            return Decimal(value)
        except (ValueError, InvalidOperation):
            raise forms.ValidationError(
                self.error_messages['invalid'], 
                code='invalid'
            )
    
    def widget_attrs(self, widget):
        attrs = super().widget_attrs(widget)
        attrs['placeholder'] = '0,00'
        return attrs
    
class DecimalInputWidget(forms.TextInput):
    """Widget personalizado para campos decimais com formatação BR"""
    
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
        return f"{float(value):.2f}".replace('.', ',')


class AccountForm(forms.ModelForm):
    """
    Formulário para criação e edição de contas
    """
    
    # Campo com maior controle sobre formatação
    original_amount = BrazilianDecimalField(
        label=_("Valor Original"),
        max_digits=15,
        decimal_places=2,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Account
        fields = [
            'type', 'category', 'document_number', 'related_responsible',
            'issue_date', 'due_date', 'description', 'original_amount',
            'is_recurring', 'installment_count', 'periodicity_days', 'specific_day_month'
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-select'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'document_number': forms.TextInput(attrs={'class': 'form-control'}),  # Adicione esta linha
            'related_responsible': forms.Select(attrs={'class': 'form-select'}),
            'issue_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'is_recurring': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'installment_count': forms.NumberInput(attrs={'class': 'form-control', 'min': '2'}),
            'periodicity_days': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'specific_day_month': forms.NumberInput(attrs={'class': 'form-control', 'min': '1', 'max': '31'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Data de emissão padrão é hoje
        if not self.instance.pk:  # Apenas para novos registros
            self.initial['issue_date'] = timezone.now().date()
        
        # Formatar o valor inicial com vírgula se existir
        if self.instance.pk and self.instance.original_amount:
            self.initial['original_amount'] = str(self.instance.original_amount).replace('.', ',')
        
        # Campos não obrigatórios
        self.fields['description'].required = False
        
        # Filtra apenas responsáveis ativos
        if 'related_responsible' in self.fields:
            try:
                self.fields['related_responsible'].queryset = Responsible.objects.filter(is_active=True)
                self.fields['related_responsible'].empty_label = "Selecione um responsável"
            except:
                # Fallback se a tabela não existir
                self.fields['related_responsible'].queryset = Responsible.objects.none()
       
    def clean(self):
        """
        Validates the form data ensuring business rules are followed.
        
        Checks:
        - Due date is not before issue date
        - Recurring settings are properly configured
        
        Returns:
            dict: Cleaned data if validation passes
            
        Raises:
            ValidationError: If validation fails
        """
        cleaned_data = super().clean()
        
        # Due date validation
        issue_date = cleaned_data.get('issue_date')
        due_date = cleaned_data.get('due_date')
        
        if issue_date and due_date and due_date < issue_date:
            self.add_error('due_date', _("Data de vencimento não pode ser anterior à data de emissão."))
        
        # Recurring settings validation
        is_recurring = cleaned_data.get('is_recurring')
        if is_recurring:
            installment_count = cleaned_data.get('installment_count')
            periodicity_days = cleaned_data.get('periodicity_days')
            specific_day_month = cleaned_data.get('specific_day_month')
            
            if not installment_count or installment_count < 2:
                self.add_error('installment_count', _("Para contas recorrentes, o número de parcelas deve ser pelo menos 2."))
            
            if not periodicity_days and not specific_day_month:
                self.add_error('periodicity_days', _("Você deve definir a periodicidade (em dias ou dia específico do mês)."))
            
            if periodicity_days and specific_day_month:
                self.add_error('periodicity_days', _("Escolha apenas um tipo de periodicidade."))
        
        return cleaned_data
    