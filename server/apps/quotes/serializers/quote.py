from rest_framework import serializers

from ..models import Quote


class QuoteRetrieveSerializer(serializers.ModelSerializer):

    class Meta:
        model = Quote
        fields = ('id', 'text')
