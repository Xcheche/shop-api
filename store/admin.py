from django.contrib import admin
from .models import *

# Register your models here.


class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "sale_start", "sale_end")
    search_fields = ("name",)

    list_editable = ("price", "sale_start", "sale_end")


admin.site.register(Product, ProductAdmin)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
