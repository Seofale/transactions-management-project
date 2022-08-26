from decimal import Decimal

from django.db.models import Manager, Q, Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone

from ..querysets import TargetUpdateQuerySet


class TargetUpdateManager(Manager):
    def get_queryset(self, **kwargs) -> TargetUpdateQuerySet:
        return TargetUpdateQuerySet(
            self.model,
            using=self._db,
        )

    def get_target_updates_sum_by_month(self, user) -> dict[str, Decimal]:
        return self.get_queryset().filter(target__user=user).aggregate(
            target_updates_sum_by_month=Coalesce(
                Sum(
                    'amount',
                    filter=Q(
                        created_date__month=timezone.now().month,
                        created_date__year=timezone.now().year
                    )
                ),
                0,
                output_field=DecimalField()
            )
        )
