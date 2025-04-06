# apps/responsibles/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.responsible_list, name='responsible-list'),
    path('create/', views.responsible_create, name='responsible-create'),
    path('<int:pk>/', views.responsible_detail, name='responsible-detail'),
    path('<int:pk>/update/', views.responsible_update, name='responsible-update'),
    path('<int:pk>/toggle-status/', views.responsible_toggle_status, name='responsible-toggle-status'),
]