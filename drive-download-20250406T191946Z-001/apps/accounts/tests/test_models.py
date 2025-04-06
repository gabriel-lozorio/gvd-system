# apps/accounts/tests/test_models.py
import pytest
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

from apps.accounts.models import Account
from apps.categories.models import Category


@pytest.fixture
def category():
    return Category.objects.create(name="Test Category")


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(username="testuser", password="password")


@pytest.mark.django_db
class TestAccount:
    def test_create_account(self, category, user):
        """Teste básico de criação de conta"""
        today = timezone.now().date()
        
        account = Account.objects.create(
            type=Account.AccountType.PAYABLE,
            category=category,
            responsible=user,
            issue_date=today,
            due_date=today + timedelta(days=30),
            description="Test account",
            original_amount=Decimal("100.00"),
        )
        
        assert account.id is not None
        assert account.type == Account.AccountType.PAYABLE
        assert account.status == Account.AccountStatus.OPEN