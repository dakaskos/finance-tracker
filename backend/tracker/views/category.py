from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from ..models.category import Category
from ..serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter
    ]
    filterset_fields = ['user', 'name']


