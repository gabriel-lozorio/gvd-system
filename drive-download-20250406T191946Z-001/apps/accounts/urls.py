from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_list, name='account-list'),
    path('create/', views.account_create, name='account-create'),
    path('<int:pk>/', views.account_detail, name='account-detail'),
    path('<int:pk>/update/', views.account_update, name='account-update'),
    path('<int:pk>/payment-form/', views.account_payment_form, name='account-payment-form'),
    path('<int:pk>/receipt-form/', views.account_receipt_form, name='account-receipt-form'),
    path('<int:pk>/register-payment/', views.account_register_payment, name='account-register-payment'),
    path('<int:pk>/register-receipt/', views.account_register_receipt, name='account-register-receipt'),
]