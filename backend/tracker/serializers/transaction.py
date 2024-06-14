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
    account_type = serializers.BooleanField(source='account.is_cash', read_only=True)

    def validate(self, data: dict) -> dict:
        amount = data['amount']
        if amount <= 0:
            raise serializers.ValidationError("Сумма должна быть больше нуля")

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
