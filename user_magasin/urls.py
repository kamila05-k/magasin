from django.urls import path
from .views import ShopListCreateView, ShopRetrieveUpdateDestroyView

urlpatterns = [
    path('shops/', ShopListCreateView.as_view(), name='shop-list-create'),
    path('shops/<int:pk>/', ShopRetrieveUpdateDestroyView.as_view(), name='shop-detail'),
]
