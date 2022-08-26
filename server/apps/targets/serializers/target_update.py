from decimal import Decimal

from rest_framework import serializers

from ..models import TargetUpdate, Target
from ...pockets.utils import create_obj_for_global_total
from ...pockets.models import Transaction
from ..constans.errors import TargetErrors


class TargetRefillSerializer(serializers.ModelSerializer):
    target = serializers.PrimaryKeyRelatedField(queryset=Target.objects.all())

    class Meta:
        model = TargetUpdate
        fields = ('amount', 'target')

    def validate_amount(self, amount: Decimal) -> Decimal:
        global_balance = create_obj_for_global_total(Transaction.objects.annotate_with_transaction_sums())['total']

        if amount > global_balance:
            raise serializers.ValidationError(TargetErrors.BALANCE_IS_NOT_ENOUGH)

        return amount

    def validate_target(self, target: Target) -> Target:
        user = self.context['request'].user

        if target.is_complete:
            raise serializers.ValidationError(TargetErrors.TARGET_IS_COMPLETE)

        if target not in user.targets.all():
            raise serializers.ValidationError(TargetErrors.NOT_USERS_TARGET)

        return target
