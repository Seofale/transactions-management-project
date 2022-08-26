from decimal import Decimal

from django.test import TestCase
from django.utils import timezone
from rest_framework.reverse import reverse

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.test import APIClient

from ..models import Target, TargetUpdate
from ...pockets.models import TransactionCategory, Transaction
from ...users.models import User
from ..utils import create_target_updates_by_percents
from ...pockets.constants import TransactionTypes


class CustomTestCase(TestCase):
    def setUp(self):
        self.user = self.create_user()

        self.category = TransactionCategory.objects.create(
            user=self.user,
            name='Тестовая категория'
        )

        Transaction.objects.create(
            user=self.user,
            category=self.category,
            amount=1000000,
            transaction_date=timezone.now().date(),
            transaction_type=TransactionTypes.INCOME
        )

        self.target = Target.objects.create(
            user=self.user,
            name='Тестовая цель',
            category=self.category,
            start_amount=100,
            amount=1000,
            term=10,
            percent=10
        )

        TargetUpdate.objects.create(
            target=self.target,
            amount=100,
        )

        self.target_create_data = {
            'name': 'Тестовая цель',
            'category': self.category.id,
            'start_amount': 100,
            'amount': 1000,
            'term': 10,
            'percent': 10
        }

        self.test_client = self.create_api_client(self.user)

    def create_user(self):
        user = User.objects.create_user(
            username='testuser',
            password='1Qaz2wsx',
            email='test@test.com',
        )

        return user

    def create_api_client(self, user):
        test_client = APIClient()

        refresh_token = RefreshToken.for_user(user)
        access_token = refresh_token.access_token

        test_client.force_authenticate(user=user, token=access_token)

        return test_client


class TargetTestFunctions(CustomTestCase):
    def setUp(self):
        super().setUp()

    def test_update_current_with_percents_for_target_by_day(self):
        expected_percents_by_day = Decimal('0.03')

        create_target_updates_by_percents()

        percents_by_day = TargetUpdate.objects.get(is_percent=True, target=self.target).amount

        self.assertEqual(
            percents_by_day,
            expected_percents_by_day,
            'Проценты за день начисляются неверно'
        )

    def test_not_update_with_percents_for_complete_target(self):
        self.target.is_complete = True
        self.target.save()

        create_target_updates_by_percents()

        is_exists_update = TargetUpdate.objects.filter(is_percent=True, target=self.target).exists()

        self.assertFalse(
            is_exists_update,
            'Проценты начисляются на завершенную цель'
        )


class TargetTestRequests(CustomTestCase):
    def setUp(self):
        super().setUp()

        self.target_complete_data = {
            'is_complete': True,
        }

        self.target_refill_data = {
            'target': self.target.id,
            'amount': 900,
        }

    def test_takes_amount_from_account_with_create_target(self):
        self.test_client.post(
            reverse('targets-list'),
            self.target_create_data,
            format='json'
        )

        transaction_expense_with_creation_exists = Transaction.objects.filter(
            amount=self.target_create_data['start_amount'],
            transaction_type=TransactionTypes.EXPENSE
        ).exists()

        self.assertTrue(
            transaction_expense_with_creation_exists,
            'Начальная сумма не списывается со счёта при создании цели'
        )

    def test_target_amount_returns_to_account_with_target_complete(self):

        self.test_client.post(
            reverse('targets-refill'),
            self.target_refill_data,
            format='json'
        )

        self.test_client.patch(
            reverse('targets-complete', kwargs={'pk': self.target.id}),
            self.target_complete_data,
            format='json'
        )

        income_transaction_with_complete_target_amount_exists = Transaction.objects.filter(
            amount=self.target_create_data['amount'],
            transaction_type=TransactionTypes.INCOME,
        ).exists()

        self.assertTrue(
            income_transaction_with_complete_target_amount_exists,
            'Накопленная сумма не возвращается после завершения цели'
        )
