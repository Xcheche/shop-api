from rest_framework.generics import (RetrieveAPIView, ListAPIView, CreateAPIView)
from store.models import Product
from .serializers import ProductSerializer


# API view to list all products
class ProductListAPIView(ListAPIView):
    """
    get:
    Return a list of all products.

    
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


# API view to retrieve a single product by ID
class ProductDetailAPIView(RetrieveAPIView):
    """
    get:
    Return a single product by ID.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'    
