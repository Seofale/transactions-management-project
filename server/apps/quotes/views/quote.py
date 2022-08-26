import random
from typing import Union

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from ..models import Quote
from ..serializers import QuoteRetrieveSerializer


class RandomQuoteRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = QuoteRetrieveSerializer

    def get_object(self) -> Union[Quote, None]:
        all_quotes = Quote.objects.all()

        if len(all_quotes) > 0:
            random_quote = random.choice(all_quotes)
            return random_quote

        return None

    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        if not self.get_object():
            return Response()

        return super().retrieve(self, request, *args, **kwargs)
