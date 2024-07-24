from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ..models.account import Account
from ..serializers.account import AccountSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
