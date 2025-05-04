# apps/core/templatetags/currency_filters.py
from django import template
from decimal import Decimal

register = template.Library()

@register.filter(name='currency_br')
def currency_br(value):
    """
    Formats a numeric value using Brazilian currency format: 1.234,56
    
    Args:
        value: The numeric value to format
        
    Returns:
        str: Formatted value with comma as decimal separator
             and period as thousands separator
    """
    if value is None:
        return "0,00"
    
    # Convert to Decimal if string
    if isinstance(value, str):
        try:
            value = Decimal(value.replace(',', '.'))
        except:
            return value
            
    # Format with two decimal places and thousands separator
    formatted_value = '{:,.2f}'.format(value).replace('.', 'X').replace(',', '.').replace('X', ',')
    return formatted_value