from django.urls import path
import store.views
from store.api_views import ProductListAPIView  # Import your API view

urlpatterns = [
    # Product details
    path('products/<int:id>/', store.views.show, name='show-product'),
    # Shopping cart
    path('cart/', store.views.cart, name='shopping-cart'),
    # Product listing or homepage
    path('', store.views.index, name='list-products'),
    # API endpoint
    path('api/products/', ProductListAPIView.as_view(), name='api-product-list'),  # Add API URL
    path('api/products/<int:id>/', store.api_views.ProductDetailAPIView.as_view(), name='api-product-detail'),  # Detail API URL
]
