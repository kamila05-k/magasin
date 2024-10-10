from rest_framework import generics, status
from django_filters import rest_framework as filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .filters import CategoryFilter, ProductFilter
from .models import *
from .serializers import *
from rest_framework.parsers import MultiPartParser, FormParser


class ProductListView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    parser_classes = [MultiPartParser, FormParser]
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
 # Здесь перечислите поля, по которым можно фильтровать

class ProductRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ProductFilter
    parser_classes = [MultiPartParser]
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Обновление продукта"""
        return super().put(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Удаление продукта"""
        return super().delete(request, *args, **kwargs)

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer  # Не забудьте создать сериализатор для Category
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CategoryFilter

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
