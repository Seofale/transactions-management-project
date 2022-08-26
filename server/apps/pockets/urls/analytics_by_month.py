from django.urls import path

from ..views import AnalyticsByMonthAPIView


urlpatterns = [
    path('analitycs_by_month/', AnalyticsByMonthAPIView.as_view()),
]
