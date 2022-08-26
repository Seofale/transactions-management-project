from django.db.models import QuerySet, Sum, F, DecimalField
from django.db.models.functions import Coalesce


class TargetQuerySet(QuerySet):
    def get_top3_targets(self) -> 'TargetQuerySet':
        return self.annotate(
            sum_target_updates=Coalesce(
                Sum('updates__amount'),
                0,
                output_field=DecimalField()
            ),
            percents_target_complete=Sum(
                    'updates__amount',
                )/F('amount')*100
        ).order_by('-percents_target_complete')[:3]
