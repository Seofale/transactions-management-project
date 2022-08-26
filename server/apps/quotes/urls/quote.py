from django.urls import path

from ..views import RandomQuoteRetrieveAPIView


urlpatterns = [
    path('random_quote/', RandomQuoteRetrieveAPIView.as_view()),
]
