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

    def update(self, instance: Transaction, validated_data: dict) -> Transaction:
        amount = validated_data.get('amount')
        if amount is not None:
            if validated_data.get('account') != instance.account:
                new_account = validated_data['account']
                if instance.type == TransactionType.EXPENSE.value:
                    new_account.balance -= amount
                else:
                    new_account.balance += amount
                old_account = instance.account
                if instance.type == TransactionType.EXPENSE.value:
                    old_account.balance += instance.amount
                else:
                    old_account.balance -= instance.amount
                new_account.save()
                old_account.save()
            else:
                account = instance.account
                diff = amount - instance.amount
                if diff != 0:
                    if instance.type == TransactionType.EXPENSE.value:
                        account.balance -= diff
                    else:
                        account.balance += diff
                    account.save()

        return super().update(instance, validated_data)

    def destroy(self, instance: Transaction) -> None:
        account = instance.account
        if instance.type == TransactionType.EXPENSE.value:
            account.balance += instance.amount
        else:
            account.balance -= instance.amount
        account.save()

        instance.delete()