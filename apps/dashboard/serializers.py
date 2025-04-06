# apps/dashboard/serializers.py
from rest_framework import serializers


class DashboardSummarySerializer(serializers.Serializer):
    """Serializer para o resumo do dashboard"""
    total_payable = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_receivable = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_paid = serializers.DecimalField(max_digits=15, decimal_places=2)
    total_received = serializers.DecimalField(max_digits=15, decimal_places=2)
    overdue_payables = serializers.IntegerField()
    overdue_receivables = serializers.IntegerField()
    projected_balance = serializers.DecimalField(max_digits=15, decimal_places=2)
    actual_balance = serializers.DecimalField(max_digits=15, decimal_places=2)