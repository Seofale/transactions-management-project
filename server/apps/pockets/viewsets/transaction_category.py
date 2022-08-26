from typing import Type, Union

from rest_framework import serializers, mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from django_filters import rest_framework as filters
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import TransactionCategory
from ..serializers import (
    TransactionCategorySerializer,
    TransactionCategorySumSerializer,
)
from ..filters import TransactionCategoryFilter
from ..models.querysets import TransactionCategoryQuerySet


class TransactionCategoryViewSet(mixins.CreateModelMixin,
                                 mixins.ListModelMixin,
                                 viewsets.GenericViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)

    def get_serializer_class(self) -> Type[serializers.ModelSerializer]:
        serializer_class = TransactionCategorySerializer

        if self.action in ('transactions_by_categories', 'transactions_by_categories_top3'):
            serializer_class = TransactionCategorySumSerializer

        return serializer_class

    @property
    def filterset_class(self):
        if self.action == 'transactions_by_categories':
            return TransactionCategoryFilter
        return None

    def get_queryset(self) -> Union[TransactionCategoryQuerySet, list]:
        queryset = TransactionCategory.objects.filter(
            user=self.request.user,
        ).annotate_with_transaction_sums().order_by(
            '-transactions_sum'
        )

        if self.action == 'transactions_by_categories':

            queryset = TransactionCategory.objects.filter(
                user=self.request.user,
            ).annotate_with_transaction_sums()

        elif self.action == 'transactions_by_categories_top3':
            queryset = TransactionCategory.objects.filter(
                user=self.request.user,
            ).get_top3_category_by_transactions_sum()

        return queryset

    @action(methods=('GET',), detail=False, url_path='categories-top3')
    def transactions_by_categories_top3(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)

    @action(
        methods=('GET',),
        detail=False,
        url_path='transactions-by-categories',
        pagination_class=None,
    )
    def transactions_by_categories(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
