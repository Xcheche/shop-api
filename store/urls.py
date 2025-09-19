from django.urls import path
import store.views
from store.api_views import ProductListAPIView  # Import your API view

urlpatterns = [
    path('products/<int:id>/', store.views.show, name='show-product'),
    path('cart/', store.views.cart, name='shopping-cart'),
    path('', store.views.index, name='list-products'),
    # API endpoint
    path('api/products/', ProductListAPIView.as_view(), name='api-product-list'),  # Add API URL
    path('api/products/<int:id>/', store.api_views.ProductDetailAPIView.as_view(), name='api-product-detail'),  # Detail API URL
]
