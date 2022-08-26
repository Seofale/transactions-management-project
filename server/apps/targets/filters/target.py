from django_filters import rest_framework as filters

from ..models import Target


class TargetFilter(filters.FilterSet):
    ordering = filters.OrderingFilter(
        fields=(
            ('start_date', 'start_date'),
            ('percent', 'percent'),
            ('amount', 'amount'),
            ('updates__amount', 'completeness')
        ))

    class Meta:
        model = Target
        fields = ('start_date', 'percent', 'amount')
