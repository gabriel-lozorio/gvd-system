# apps/dashboard/urls.py
from django.urls import path
from apps.dashboard import views
from apps.dashboard import api

urlpatterns = [
    # Views HTML
    path('', views.dashboard, name='dashboard'),
    path('summary-partial/', views.dashboard_summary_partial, name='dashboard-summary-partial'),
    
    # APIs REST
    path('api/summary/', api.DashboardSummaryView.as_view(), name='api-dashboard-summary'),
    path('api/evolution/', api.MonthlyEvolutionView.as_view(), name='api-monthly-evolution'),
]