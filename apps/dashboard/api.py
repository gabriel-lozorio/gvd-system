# apps/dashboard/api.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.dashboard.services import DashboardService
from apps.dashboard.serializers import DashboardSummarySerializer


class DashboardSummaryView(APIView):
    """
    View para resumo do dashboard
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """Retorna o resumo do dashboard"""
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        
        if year:
            year = int(year)
        if month:
            month = int(month)
        
        summary_data = DashboardService.get_monthly_summary(year, month)
        serializer = DashboardSummarySerializer(summary_data)
        
        category_data = DashboardService.get_category_summary(year, month)
        
        return Response({
            "summary": serializer.data,
            "categories": category_data
        })


class MonthlyEvolutionView(APIView):
    """
    View para evolução mensal
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, format=None):
        """Retorna a evolução mensal"""
        months = request.query_params.get('months', 6)
        months = int(months)
        
        evolution_data = DashboardService.get_monthly_evolution(months)
        
        return Response(evolution_data)