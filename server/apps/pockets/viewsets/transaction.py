from decimal import Decimal
from typing import Type, Union

from django.http import HttpResponse
from django.utils import timezone
from rest_framework import viewsets, serializers, pagination, status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django_filters import rest_framework as filters
from openpyxl.writer.excel import save_virtual_workbook

from ..models import Transaction
from ..models.querysets import TransactionQuerySet
from ..serializers import (
    TransactionCreateSerializer,
    TransactionRetrieveSerializer,
    TransactionGlobalSerializer,
    TransactionGlobalTotalSerializer,
)
from ..filters import TransactionFilter
from ..utils import (create_obj_for_global_total, save_transactions_as_xlsx,
                     create_transactions_by_xlsx_file)
from ..constants import SendingFilesHeaders


class TransactionViewSet(viewsets.ModelViewSet):
    pagination_class = pagination.LimitOffsetPagination
    pagination_class.default_limit = 20
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TransactionFilter
    parser_classes = (MultiPartParser,)

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        if self.action == 'total':
            serializer_class = TransactionGlobalSerializer
        elif self.action in {'create', 'update', 'partial_update'}:
            serializer_class = TransactionCreateSerializer
        elif self.action == 'global_total':
            serializer_class = TransactionGlobalTotalSerializer
        else:
            serializer_class = TransactionRetrieveSerializer

        return serializer_class

    def get_queryset(self) -> TransactionQuerySet:

        if self.action == 'transactions_export':
            return Transaction.objects.filter(
                user=self.request.user,
            )

        queryset = Transaction.objects.filter(
                user=self.request.user,
            ).select_related(
            'category',
        ).order_by(
            '-transaction_date', '-id',
        )

        return queryset

    def get_object(self) -> Union[Transaction, dict[str, Decimal]]:
        if self.action == 'total':
            obj = self.filter_queryset(self.get_queryset()).aggregate_totals()
        elif self.action == 'global_total':
            obj_aggregate_totals = self.filter_queryset(self.get_queryset()).aggregate_totals()
            obj = create_obj_for_global_total(obj_aggregate_totals)
        else:
            obj = super().get_object()

        return obj

    @action(
        methods=('GET',),
        detail=False,
        url_path='global',
    )
    def total(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='global-total')
    def global_total(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(methods=('GET',), detail=False, url_path='transactions-export')
    def transactions_export(self, request: Request) -> HttpResponse:
        queryset = self.filter_queryset(self.get_queryset())
        workbook = save_transactions_as_xlsx(queryset)

        response = HttpResponse(
            content=save_virtual_workbook(workbook),
            content_type=SendingFilesHeaders.CONTENT_TYPE_XLSX
        )
        response['Content-Disposition'] = f'attachment; filename={request.user}--{timezone.now()}.xlsx'
        return response

    @action(
        methods=('POST',),
        detail=False,
        url_path='transactions-import',
        parser_classes=(MultiPartParser,),
    )
    def transactions_import(self, request: Request) -> Response:
        file_obj = request.data['file']
        errors = create_transactions_by_xlsx_file(file_obj=file_obj, request=request)

        if errors:
            return Response(
                {"errors": errors},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(status=status.HTTP_201_CREATED)
