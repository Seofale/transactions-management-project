from typing import Type

from django.utils import timezone
from rest_framework import viewsets, serializers, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from django_filters import rest_framework as filters

from ..serializers import (TargetCreateSerializer, TargetRefillSerializer,
                           TargetAnalyticsSerializer, TargetCompleteSerializer)
from ..models import Target, TargetUpdate
from ..serializers import TargetRetrieveSerializer, TargetUpdateSerializer, TargetTopSerializer
from ...pockets.models import Transaction
from ..utils import get_sum_amount_updates
from ..filters import TargetFilter


class TargetViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthenticated,)
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = TargetFilter

    def get_serializer_class(self) -> Type[serializers.Serializer]:
        serializer_class = TargetRetrieveSerializer
        if self.action == 'create':
            serializer_class = TargetCreateSerializer
        elif self.action in ('update', 'partial_update'):
            serializer_class = TargetUpdateSerializer
        elif self.action == 'complete':
            serializer_class = TargetCompleteSerializer
        elif self.action == 'analytics':
            serializer_class = TargetAnalyticsSerializer
        elif self.action == 'top3_targets':
            serializer_class = TargetTopSerializer

        return serializer_class

    def get_queryset(self):
        if self.action == 'top3_targets':
            return Target.objects.filter(
                user=self.request.user
            ).get_top3_targets()

        return Target.objects.filter(
            user=self.request.user
        ).order_by('start_date')

    def get_object(self):
        if self.action == 'analytics':
            return Target.objects.get_analytics(user=self.request.user)
        else:
            return super().get_object()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        sum_amount_updates = get_sum_amount_updates(instance)

        Transaction.objects.create(
            user=self.request.user,
            transaction_date=timezone.now(),
            amount=sum_amount_updates,
            transaction_type='income',
        )

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(
        methods=('POST',),
        detail=False,
        url_path='refill',
    )
    def refill(self, request: Request) -> Response:
        serializer = TargetRefillSerializer(
            data=request.data,
            context={'request': self.request}
        )

        serializer.is_valid(raise_exception=True)

        TargetUpdate.objects.create(
            target_id=serializer.data['target'],
            amount=serializer.data['amount'],
        )

        Transaction.objects.create(
            user=self.request.user,
            transaction_date=timezone.now(),
            amount=serializer.data['amount'],
            transaction_type='expense'
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        methods=('PATCH',),
        detail=True,
        url_path='complete',
    )
    def complete(self, request: Request, *args, **kwargs) -> Response:
        return super().partial_update(request, *args, **kwargs)

    @action(
        methods=('GET',),
        detail=False,
        url_path='analytics',
    )
    def analytics(self, request: Request, *args, **kwargs) -> Response:
        return super().retrieve(request, *args, **kwargs)

    @action(
        methods=('GET',),
        detail=False,
        url_path='top3-targets',
    )
    def top3_targets(self, request: Request, *args, **kwargs) -> Response:
        return super().list(request, *args, **kwargs)
