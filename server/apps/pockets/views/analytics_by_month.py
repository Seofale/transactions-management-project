from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from ..serializers import AnalyticsByMonthSerializer
from ..models import Transaction


class AnalyticsByMonthAPIView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AnalyticsByMonthSerializer

    def get_object(self):
        return Transaction.objects.get_analytics_by_month(user=self.request.user)
