#Api endpoints
from rest_framework.generics import (RetrieveAPIView, ListAPIView, CreateAPIView)
#Django filters
from django_filters.rest_framework import DjangoFilterBackend
#Local imports
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
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('id',)

    #-----Query set----------------------
    def get_queryset(self):
        """Query set to filter products based on sale status."""
        on_sale = self.request.query_params.get('on_sale', None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        if on_sale.lower() == 'true':
            from django.utils import timezone
            now = timezone.now()
            return queryset.filter(
                sale_start__lte=now,
                sale_end__gte=now,
            )
        return queryset
    #To test  visit http://127.0.0.1:2020/api/products/?on_sale=true



# API view to retrieve a single product by ID
class ProductDetailAPIView(RetrieveAPIView):
    """
    get:
    Return a single product by ID.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = 'id'    
