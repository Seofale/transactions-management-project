from django_filters import rest_framework as filters

from ..models import Transaction


class TransactionFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name='transaction_date__year', lookup_expr='exact')
    month = filters.NumberFilter(field_name='transaction_date__month', lookup_expr='exact')
    ordering = filters.OrderingFilter(
        fields=(
            ('transaction_date', 'transaction_date'),
            ('category', 'category'),
            ('amount', 'amount'),
        ))

    class Meta:
        model = Transaction
        fields = ('transaction_date', 'category', 'amount')
