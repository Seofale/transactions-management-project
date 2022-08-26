from decimal import Decimal

from django.db.models import Manager
from django.utils import timezone

from ..querysets import TransactionQuerySet
from ....targets import models as targets_models
from ....pockets import models as pockets_models


class TransactionManager(Manager):
    def get_queryset(self, **kwargs) -> TransactionQuerySet:
        return TransactionQuerySet(
            self.model,
            using=self._db,
        )

    def annotate_with_transaction_sums(self) -> dict[str, Decimal]:
        return self.get_queryset().aggregate_totals()

    def get_income_and_expense_transactions_sum_by_month(self, user) -> dict[str, Decimal]:
        return self.get_queryset().filter(
            user=user,
            transaction_date__month=timezone.now().month,
            transaction_date__year=timezone.now().year
        ).aggregate_totals()

    def get_target_updates_sum_by_month(self, user) -> dict[str, Decimal]:
        return targets_models.TargetUpdate.objects.get_target_updates_sum_by_month(user=user)

    def get_category_with_most_amount_by_month(self, user) -> int:
        return pockets_models.TransactionCategory.objects.filter(
            user=user
        ).annotate_with_transaction_sums().order_by('-transactions_sum').first().id

    def get_analytics_by_month(self, user):
        analytics_data = {}

        analytics_data.update(self.get_income_and_expense_transactions_sum_by_month(user=user))

        analytics_data.update(self.get_target_updates_sum_by_month(user=user))

        analytics_data.update(
            {'category_with_most_amount_by_month': self.get_category_with_most_amount_by_month(user=user)}
        )

        return analytics_data
