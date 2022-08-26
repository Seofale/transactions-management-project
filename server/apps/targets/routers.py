from rest_framework.routers import DefaultRouter

from .viewsets import TargetViewSet

targets_router = DefaultRouter()

targets_router.register(
    prefix='targets',
    viewset=TargetViewSet,
    basename='targets',
)
