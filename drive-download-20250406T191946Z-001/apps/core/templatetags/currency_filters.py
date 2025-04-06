# apps/core/templatetags/currency_filters.py
from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='currency_br')
def currency_br(value):
    """
    Formata um valor numérico no padrão de moeda brasileira: 1.234,56
    """
    if value is None:
        return "0,00"
    
    # Converte para Decimal se for string
    if isinstance(value, str):
        try:
            value = Decimal(value.replace(',', '.'))
        except:
            return value
            
    # Formata com duas casas decimais e separador de milhar
    valor_formatado = '{:,.2f}'.format(value).replace('.', 'X').replace(',', '.').replace('X', ',')
    return valor_formatado