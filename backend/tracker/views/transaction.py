from django_filters.rest_framework import DjangoFilterBackend
from django_filters import rest_framework
from rest_framework import viewsets, filters

from ..models.transaction import Transaction
from ..serializers.transaction import TransactionSerializer


class TransactionFilter(rest_framework.FilterSet):
    start_date = rest_framework.DateFilter(field_name='date', lookup_expr='gte')
    end_date = rest_framework.DateFilter(field_name='date', lookup_expr='lte')

    class Meta:
        model = Transaction
        fields = ['user', 'category', 'type', 'account', 'start_date', 'end_date']


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
