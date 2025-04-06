# app/categories/forms.py

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Category

class CategoryForm(forms.ModelForm):
    """
    Formulário para criação e edição de categorias
    """
    
    class Meta:
        model = Category
        fields = ['name', 'description', 'parent']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adiciona classes do Bootstrap aos campos
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Evitar que uma categoria seja pai dela mesma na edição
        if kwargs.get('instance'):
            instance = kwargs['instance']
            self.fields['parent'].queryset = Category.objects.exclude(pk=instance.pk)