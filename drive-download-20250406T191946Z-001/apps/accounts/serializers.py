# apps/accounts/serializers.py
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import Account
from apps.categories.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer para categorias"""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'parent', 'full_path']
        read_only_fields = ['full_path']


class AccountSerializer(serializers.ModelSerializer):
    """Serializer para contas"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    responsible_name = serializers.CharField(source='responsible.get_full_name', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    type_display = serializers.CharField(source='get_type_display', read_only=True)
    is_overdue = serializers.BooleanField(read_only=True)
    days_overdue = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = Account
        fields = [
            'id', 'type', 'type_display', 'category', 'category_name', 
            'document_number', 'responsible', 'responsible_name', 
            'issue_date', 'due_date', 'description', 'original_amount', 
            'status', 'status_display', 'is_recurring', 'installment_count',
            'periodicity_days', 'specific_day_month', 'parent_installment',
            'is_overdue', 'days_overdue', 'created_at', 'updated_at'
        ]
        read_only_fields = ['status', 'is_overdue', 'days_overdue']
    
    def validate(self, data):
        """Validações adicionais"""
        # Verifica data de vencimento
        if data.get('due_date') and data.get('issue_date'):
            if data['due_date'] < data['issue_date']:
                raise serializers.ValidationError(
                    _("Data de vencimento não pode ser anterior à data de emissão")
                )
        
        # Verifica campos de recorrência
        if data.get('is_recurring'):
            if not data.get('installment_count'):
                raise serializers.ValidationError(
                    _("Número de parcelas é obrigatório para contas recorrentes")
                )
            
            if not (data.get('periodicity_days') or data.get('specific_day_month')):
                raise serializers.ValidationError(
                    _("É necessário definir a periodicidade (em dias ou dia do mês)")
                )
        
        return data

