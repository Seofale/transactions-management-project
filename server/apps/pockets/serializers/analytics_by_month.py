from rest_framework import serializers


class AnalyticsByMonthSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)
    target_updates_sum_by_month = serializers.DecimalField(max_digits=12, decimal_places=2)
    category_with_most_amount_by_month = serializers.IntegerField()
