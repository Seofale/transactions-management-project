from decimal import Decimal

from django.db.models import QuerySet, Sum, DecimalField, Count, Q, Max
from django.db.models.functions import Coalesce

from ...constants import TransactionCategoryConsts


class TransactionCategoryQuerySet(QuerySet):
    def annotate_with_transaction_sums(self):
        """
        :return: TransactionCategoryQuerySet
        """

        return self.annotate(
            transactions_sum=Coalesce(
                Sum('transactions__amount'),
                0,
                output_field=DecimalField(),
            ),
        )

    def get_top3_category_by_transactions_sum(self) -> list[dict[str, Decimal]]:

        queryset = self.annotate_with_transaction_sums().order_by(
            '-transactions_sum'
        )
        queryset_top3 = list(
            queryset[:TransactionCategoryConsts.CATEGORY_TOP_COUNT].values_list(
                'name', 'transactions_sum',
            )
        )
        anothers = queryset[TransactionCategoryConsts.CATEGORY_TOP_COUNT:].aggregate(
            transactions_sums=Coalesce(
                Sum('transactions__amount'),
                0,
                output_field=DecimalField(),
            ),
        )

        queryset_top3.append(
            {
                'name': 'Другое',
                'transactions_sum': anothers['transactions_sums'],
            }
        )

        return queryset_top3

    def get_most_successful_category_by_targets(self) -> int:
        return self.annotate(
                    target_count=Count(
                        'targets',
                        filter=Q(
                            targets__is_complete=True
                        ),
                    )
                ).order_by('-target_count').first().id

    def get_most_popular_category_by_targets(self) -> int:
        return self.annotate(
                    target_count=Count(
                        'targets',
                    )
                ).order_by('target_count').first().id
