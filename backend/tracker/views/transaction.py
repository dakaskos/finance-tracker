from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from rest_framework import viewsets, filters, status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from ..models.transaction import Transaction, TransactionType
from ..serializers.transaction import TransactionSerializer


class TransactionFilter(rest_framework.FilterSet):
    start_date = rest_framework.DateFilter(field_name='date', lookup_expr='gte')
    end_date = rest_framework.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['user', 'type', 'account', 'start_date', 'end_date']


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = TransactionFilter
    ordering_fields = ['date', 'id']
    permission_classes = [IsAuthenticatedOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        account = instance.account
        if instance.type == TransactionType.EXPENSE.value:
            account.balance += instance.amount
        else:
            account.balance -= instance.amount
        account.save()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

