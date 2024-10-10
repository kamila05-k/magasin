from django.urls import path
from .views import *

urlpatterns = [
    # Продукты
    path('/products/', ProductListView.as_view(), name='product-list'),
    path('/products/<int:pk>/', ProductRetrieveUpdateDestroyView.as_view(), name='product-detail'),
    path('categories', CategoryListView.as_view(), name='category-list'),
]
