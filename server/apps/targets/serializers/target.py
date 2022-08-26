from decimal import Decimal
from datetime import date

from django.utils import timezone

from rest_framework import serializers

from ...pockets.models import TransactionCategory
from ...pockets.models import Transaction
from ...pockets.utils import create_obj_for_global_total
from ..models import Target
from ..constans import TargetErrors
from ..models import TargetUpdate
from ...pockets.serializers import TransactionCategorySerializer
from ..utils import get_sum_amount_updates
from ...pockets.constants import TransactionCategoryErrors
from ..add_months import add_months_to_date


class TargetTopSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer(allow_null=True)
    percents_target_complete = serializers.IntegerField()
    sum_target_updates = serializers.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        model = Target
        fields = (
            'id',
            'name',
            'category',
            'amount',
            'term',
            'percent',
            'start_date',
            'is_complete',
            'sum_target_updates',
            'percents_target_complete',
        )


class TargetRetrieveSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer(allow_null=True)
    target_updates_sum = serializers.SerializerMethodField()
    days_to_end = serializers.SerializerMethodField()

    class Meta:
        model = Target
        fields = (
            'id',
            'name',
            'category',
            'amount',
            'term',
            'percent',
            'start_date',
            'is_complete',
            'target_updates_sum',
            'days_to_end'
        )

    def get_target_updates_sum(self, obj):
        return get_sum_amount_updates(obj)

    def get_days_to_end(self, obj):
        return obj.get_days_to_end


class TargetUpdateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=TransactionCategory.objects.all(), required=False)

    class Meta:
        model = Target
        fields = ('name', 'category', 'amount', 'term', 'percent',)

    def validate_amount(self, amount) -> Decimal:
        sum_amount_updates = get_sum_amount_updates(self.instance)
        if amount < sum_amount_updates:
            raise serializers.ValidationError(TargetErrors.CANT_CHANGE_AMOUNT)
        return amount

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category and category not in user.categories.all():
            raise serializers.ValidationError(TransactionCategoryErrors.NOT_USERS_CATEGORY)
        else:
            return category

    def validate_term(self, term: int) -> int:
        end_date = add_months_to_date(self.instance.start_date, self.instance.term)
        new_end_date = add_months_to_date(date.today(), term)

        if end_date > new_end_date:
            raise serializers.ValidationError(TargetErrors.THIS_TERM_PASSED)
        return term

    def validate(self, attrs: dict) -> dict:
        if self.instance.is_complete:
            raise serializers.ValidationError(TargetErrors.TARGET_IS_COMPLETE)
        return attrs

    def update(self, instance: Target, validated_data: dict) -> Target:
        instance.name = validated_data.get('name', instance.name)
        instance.category = validated_data.get('category', instance.category)
        instance.amount = validated_data.get('amount', instance.amount)
        instance.term = validated_data.get('term', instance.term)
        instance.percent = validated_data.get('percent', instance.percent)
        instance.save()
        return instance


class TargetCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=TransactionCategory.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Target
        fields = ('id', 'name', 'category', 'start_amount', 'amount', 'term', 'percent',)

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category and category not in user.categories.all():
            raise serializers.ValidationError(TransactionCategoryErrors.NOT_USERS_CATEGORY)
        else:
            return category

    def validate(self, attrs: dict) -> dict:
        global_balance = create_obj_for_global_total(Transaction.objects.annotate_with_transaction_sums())['total']

        if 0 <= attrs['start_amount'] <= global_balance:
            return attrs
        else:
            raise serializers.ValidationError(TargetErrors.BALANCE_IS_NOT_ENOUGH)

    def create(self, validated_data: dict) -> Target:
        validated_data['user'] = self.context['request'].user
        start_amount = validated_data['start_amount']

        target = Target.objects.create(**validated_data)

        if start_amount > 0:
            Transaction.objects.create(
                user=self.context['request'].user,
                category=validated_data.get('category'),
                transaction_date=timezone.now(),
                amount=start_amount,
                transaction_type='expense',
            )

            TargetUpdate.objects.create(
                target=target,
                amount=start_amount,
            )

        return target


class TargetCompleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Target
        fields = ('is_complete',)

    def validate(self, attrs):
        user = self.context['request'].user
        target = self.instance

        if target not in user.targets.all():
            raise serializers.ValidationError(TargetErrors.NOT_USERS_TARGET)

        if target.is_complete:
            raise serializers.ValidationError(TargetErrors.TARGET_IS_COMPLETE)

        return attrs

    def update(self, instance, validated_data):
        user = self.context['request'].user
        sum_amount_updates = get_sum_amount_updates(instance)

        if instance.is_complete:
            raise serializers.ValidationError(TargetErrors.TARGET_IS_COMPLETE)

        if sum_amount_updates >= instance.amount:

            Transaction.objects.create(
                user=user,
                transaction_date=timezone.now(),
                amount=sum_amount_updates,
                transaction_type='income'
            )

            instance.is_complete = True
            instance.complete_date = timezone.now()
            instance.save()
            return instance

        raise serializers.ValidationError(TargetErrors.TARGET_BALANSE_IS_NOT_ENOUGH)


class TargetAnalyticsSerializer(serializers.Serializer):
    not_complete_targets_count = serializers.IntegerField()
    sum_not_complete_targets = serializers.DecimalField(max_digits=12, decimal_places=2)
    sum_percents_not_complete_targets = serializers.DecimalField(max_digits=12, decimal_places=2)
    sum_not_complete_targets_by_month = serializers.DecimalField(max_digits=12, decimal_places=2)
    days_to_closest_target = serializers.IntegerField()
    most_successful_category = serializers.IntegerField(allow_null=True)
    most_popular_category = serializers.IntegerField(allow_null=True)

