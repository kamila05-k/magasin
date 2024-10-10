import django_filters
from .models import *


class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='icontains')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.all())
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')

    class Meta:
        model = Product
        fields = ['name', 'category', 'price_min', 'price_max','store_name']

class CategoryFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Category
        fields = ['id']