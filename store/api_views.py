# Api endpoints
from django.forms import ValidationError  # noqa
from rest_framework.generics import (
    RetrieveAPIView,
    ListAPIView,
    CreateAPIView,
    RetrieveUpdateDestroyAPIView,
)

# Django filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

# Local imports
from store.models import Product
from .serializers import ProductSerializer
from rest_framework.pagination import LimitOffsetPagination


# Pagination class
class ProductLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 10  # Default number of items to return
    max_limit = 100  # Maximum number of items that can be requested


# API view to list all products
class ProductListAPIView(ListAPIView):
    """
    get:
    Return a list of all products.


    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("id",)
    # Adding limit offset pagination To test visit http://127.0.0.1:8000/api/products/?limit=5&offset=0 OR  1
    pagination_class = ProductLimitOffsetPagination

    # -----Query set search by sale status----------------------
    def get_queryset(self):
        """Query set to filter products based on sale status."""
        on_sale = self.request.query_params.get("on_sale", None)
        if on_sale is None:
            return super().get_queryset()
        queryset = Product.objects.all()
        if on_sale.lower() == "true":
            from django.utils import timezone

            now = timezone.now()
            return queryset.filter(
                sale_start__lte=now,
                sale_end__gte=now,
            )
        return queryset

    # -------------------------------To test  visit http://127.0.0.1:2020/api/products/?on_sale=true-----------------------------------#
    # ------For filter 1 search
    # filter_backends = (DjangoFilterBackend,)
    # filterset_fields = ('id','description',)

    # ------For search 2
    filter_backends = (filters.SearchFilter,)

    """search_fields = ('^id','^title','^content',)  # ^ startswith, = exact, @ full-text search (postgres only)
    """
    # =Exact match
    search_fields = (
        "=id",
        "=name",
        "=description",
    )

    # ^Startswith
    # search_fields = ('^id','^title','^content',)

    # @ Full text search (Postgres only)
    # search_fields = ('@id','@title','@content',)

    # =======Using Ordering filter
    # filter_backends = (filters.OrderingFilter,)
    # ordering_fields = ('id','name',)  # fields to be ordered
    # ordering = ('id',)  # default ordering


# API view to retrieve a single product by ID
class ProductDetailAPIView(RetrieveAPIView):
    """
    get:
    Return a single product by ID.
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    lookup_field = "id"  # Lookup field for retrieving a product by ID


# Create product
class ProductCreate(CreateAPIView):
    serializer_class = ProductSerializer

    def create(self, request, *args, **kwargs):
        try:
            price = request.data.get("price")
            if price is not None and float(price) <= 0.0:
                raise ValidationError({"price": "Must be above $0.00"})
        except ValueError:
            raise ValidationError({"price": "A valid number is required"})
        return super().create(request, *args, **kwargs)


# Retrieve update delete


class ProductRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    lookup_field = "id"
    serializer_class = ProductSerializer

    # Override delete  methods to clear cache if implemented
    def delete(self, request, *args, **kwargs):
        product_id = request.data.get("id")
        response = super().delete(request, *args, **kwargs)
        if response.status_code == 204:
            from django.core.cache import cache

            cache.delete("product_data_{}".format(product_id))
        return response

    # Override update method to update cache if implemented
    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        if response.status_code == 200:
            from django.core.cache import cache

            product = response.data
            cache.set(
                "product_data_{}".format(product["id"]),
                {
                    "name": product["name"],
                    "description": product["description"],
                    "price": product["price"],
                },
            )
        return response
