from rest_framework import serializers, fields

from ..models.transaction import Transaction, TransactionType


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    currency = serializers.CharField(source='account.currency', read_only=True)
    type = fields.ChoiceField(
        choices=[(tag.value, tag.name) for tag in TransactionType]
    )
    category_name = serializers.CharField(source='category.name', read_only=True)
    account_type = serializers.BooleanField(source='account.is_cash', read_only=True)

    def validate(self, data: dict) -> dict:
        amount = data['amount']
        if amount <= 0:
            raise serializers.ValidationError("Amount must be greater than zero.")

        account = data['account']
        transaction_type = data['type']

        if (account.balance - amount < 0
                and transaction_type == TransactionType.EXPENSE.value
        ):
            error_message = "Account balance must be greater than zero."
            raise serializers.ValidationError(error_message)

        return data

    def create(self, validated_data: dict) -> Transaction:
        account = validated_data['account']
        amount = validated_data['amount']
        transaction_type = validated_data['type']

        if transaction_type == TransactionType.EXPENSE.value:
            account.balance -= amount
        else:
            account.balance += amount

        account.save()

        return Transaction.objects.create(**validated_data)
