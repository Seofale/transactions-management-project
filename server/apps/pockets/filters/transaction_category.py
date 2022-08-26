from django_filters import rest_framework as filters


class TransactionCategoryFilter(filters.FilterSet):
    year = filters.NumberFilter(field_name='transactions__transaction_date__year', lookup_expr='exact')
    month = filters.NumberFilter(field_name='transactions__transaction_date__month', lookup_expr='exact')
