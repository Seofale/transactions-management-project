from django.urls import path

from ..views import UserSummaryAPIView


urlpatterns = [
    path('me/', UserSummaryAPIView.as_view()),
]
