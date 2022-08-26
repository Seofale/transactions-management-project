from decimal import Decimal

from django.db.models import Sum, DecimalField
from django.db.models.functions import Coalesce

from ..models import Target, TargetUpdate


def get_sum_amount_updates(instance: Target) -> Decimal:
    return instance.updates.aggregate(
            amount_updates=Sum('amount'),
        )['amount_updates']


def create_target_updates_by_percents():

    target_updates = []

    for target in Target.objects.filter(is_complete=False):
        now_target_balance = target.updates.aggregate(
            amounts_sum=Coalesce(
                Sum(
                    'amount',
                ),
                0,
                output_field=DecimalField(),
            ),
        )['amounts_sum']

        if now_target_balance == 0:
            continue

        percents_by_day = (now_target_balance / 100) * Decimal(target.percent / 365)

        target_update = TargetUpdate(
            target=target,
            amount=percents_by_day,
            is_percent=True
        )
        target_updates.append(target_update)

    TargetUpdate.objects.bulk_create(target_updates)
