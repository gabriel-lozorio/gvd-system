# apps/responsibles/forms.py
from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Responsible


class ResponsibleForm(forms.ModelForm):
    """
    Formulário para criação e edição de responsáveis
    """
    
    class Meta:
        model = Responsible
        fields = ['name', 'email', 'phone', 'notes', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def clean_email(self):
        """Validação para garantir email único quando informado"""
        email = self.cleaned_data.get('email')
        if email:
            # Verificar se já existe outro responsável com este email
            qs = Responsible.objects.filter(email=email)
            if self.instance.pk:
                qs = qs.exclude(pk=self.instance.pk)
            
            if qs.exists():
                raise forms.ValidationError(_("Já existe um responsável com este email."))
        
        return email
    
    def clean_phone(self):
        """Normaliza o telefone, removendo caracteres não numéricos"""
        phone = self.cleaned_data.get('phone')
        if phone:
            # Remove caracteres não numéricos
            phone = ''.join([c for c in phone if c.isdigit()])
            
            # Formata o telefone
            if len(phone) == 11:  # Celular com DDD
                phone = f"({phone[:2]}) {phone[2:7]}-{phone[7:]}"
            elif len(phone) == 10:  # Telefone fixo com DDD
                phone = f"({phone[:2]}) {phone[2:6]}-{phone[6:]}"
                
        return phone