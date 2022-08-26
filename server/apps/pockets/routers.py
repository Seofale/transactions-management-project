from rest_framework.routers import DefaultRouter

from .viewsets import TransactionViewSet, TransactionCategoryViewSet

pockets_router = DefaultRouter()

pockets_router.register(
    prefix='transactions',
    viewset=TransactionViewSet,
    basename='transactions',
)
pockets_router.register(
    prefix='categories',
    viewset=TransactionCategoryViewSet,
    basename='categories',
)
