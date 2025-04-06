from django.contrib import admin
from .models import Payment, Receipt

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['account']

@admin.register(Receipt)
class ReceiptAdmin(admin.ModelAdmin):
    list_display = ['account']