from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from ..models.account import Account
from ..serializers.account import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
