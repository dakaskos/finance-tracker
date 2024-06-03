from rest_framework import serializers, fields

from ..entities.currency import Currency
from ..models.account import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

    currency = fields.ChoiceField(choices=[(tag.value, tag.name) for tag in Currency])
