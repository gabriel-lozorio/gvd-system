from django.contrib import admin
from .models import Account

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    # Use apenas os campos que existem no seu modelo
    list_display = ['description']
    search_fields = ['description']