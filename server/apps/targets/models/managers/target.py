from decimal import Decimal
from typing import Union

from django.db.models import Manager, Count, Q, Sum, DecimalField
from django.db.models.functions import Coalesce
from django.utils import timezone

from ..querysets import TargetQuerySet
from ....pockets import models


class TargetManager(Manager):
    def get_queryset(self, **kwargs) -> TargetQuerySet:
        return TargetQuerySet(
            self.model,
            using=self._db,
        )

    def get_not_complete_targets_count(self, user):
        return self.get_queryset().filter(user=user).aggregate(
            not_complete_targets_count=Count(
                'id',
                filter=Q(is_complete=False)
            ))

    def get_sum_not_complete_targets(self, user):
        return self.get_queryset().filter(user=user).aggregate(
            sum_not_complete_targets=Coalesce(
                Sum(
                    'updates__amount',
                    filter=Q(is_complete=False)
                ),
                0,
                output_field=DecimalField(),
            ))

    def get_sum_percents_not_complete_targets(self, user):
        return self.get_queryset().filter(user=user).aggregate(
            sum_percents_not_complete_targets=Coalesce(
                Sum(
                    'updates__amount',
                    filter=Q(updates__is_percent=True),
                ),
                0,
                output_field=DecimalField(),
            ))

    def get_sum_not_complete_targets_by_month(self, user):
        return self.get_queryset().filter(user=user).aggregate(
            sum_not_complete_targets_by_month=Coalesce(
                Sum(
                    'updates__amount',
                    filter=Q(
                        updates__is_percent=True,
                        updates__created_date__month=timezone.now().month,
                        updates__created_date__year=timezone.now().year
                    ),
                ),
                0,
                output_field=DecimalField(),
            ))

    def get_days_to_closest_target(self, user) -> Union[int, None]:

        days_to_closest_target = list(self.filter(
            is_complete=False,
            user=user
        )).sort(key=lambda x: x.get_days_to_end)

        return days_to_closest_target[0] if days_to_closest_target else None

    def get_most_successful_category(self, user):
        if self.filter(is_complete=True, user=user).count() == 0:
            most_successful_category = None
        else:
            most_successful_category = models.TransactionCategory.objects.filter(
                user=user
            ).get_most_successful_category_by_targets()

        return most_successful_category

    def get_most_popular_category(self, user):
        if self.count() == 0:
            most_popular_category = None
        else:
            most_popular_category = models.TransactionCategory.objects.filter(
                user=user
            ).get_most_popular_category_by_targets()

        return most_popular_category

    def get_analytics(self, user) -> dict[str, Union[Decimal, int, None]]:

        analytics_data = {}

        analytics_data.update(self.get_not_complete_targets_count(user=user))

        analytics_data.update(self.get_sum_not_complete_targets(user=user))

        analytics_data.update(self.get_sum_percents_not_complete_targets(user=user))

        analytics_data.update(self.get_sum_not_complete_targets_by_month(user=user))

        analytics_data.update({'days_to_closest_target': self.get_days_to_closest_target(user=user)})

        analytics_data.update({'most_successful_category': self.get_most_successful_category(user=user)})

        analytics_data.update({'most_popular_category': self.get_most_popular_category(user=user)})

        return analytics_data
