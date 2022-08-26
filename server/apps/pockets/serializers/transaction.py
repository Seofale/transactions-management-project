from collections import OrderedDict

from rest_framework import serializers

from ..constants import TransactionErrors, TransactionCategoryErrors
from ..models import Transaction, TransactionCategory
from .transaction_category import TransactionCategorySerializer


class TransactionRetrieveSerializer(serializers.ModelSerializer):
    category = TransactionCategorySerializer(allow_null=True)

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_date', 'amount', 'transaction_type')


class TransactionCreateSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(
        queryset=TransactionCategory.objects.all(),
        allow_null=True,
        required=False
    )

    class Meta:
        model = Transaction
        fields = ('id', 'category', 'transaction_date', 'amount', 'transaction_type')

    def validate_category(self, category: TransactionCategory) -> TransactionCategory:
        user = self.context['request'].user

        if category and category not in user.categories.all():
            raise serializers.ValidationError(TransactionCategoryErrors.NOT_USERS_CATEGORY)
        else:
            return category

    def validate(self, attrs: dict) -> dict:
        transaction_type = attrs['transaction_type']
        category = attrs.get('category')

        if not category and transaction_type == 'expense':
            raise serializers.ValidationError(TransactionErrors.TRANSACTION_EXPENSE_WITH_NO_CATEGORY)

        if category and transaction_type == 'income':
            raise serializers.ValidationError(TransactionErrors.TRANSACTION_INCOME_WITH_CATEGORY)

        return attrs

    def create(self, validated_data: dict) -> Transaction:
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)

    @property
    def data(self) -> OrderedDict:
        """
        Сделано для того, чтобы при создании объекта можно было передвавть id категории, а после
        создания поле категории возвращалось как объект
        """
        return TransactionRetrieveSerializer(instance=self.instance).data


class TransactionGlobalSerializer(serializers.Serializer):
    total_income = serializers.DecimalField(max_digits=12, decimal_places=2)
    total_expenses = serializers.DecimalField(max_digits=12, decimal_places=2)


class TransactionGlobalTotalSerializer(serializers.Serializer):
    total = serializers.DecimalField(max_digits=12, decimal_places=2)
