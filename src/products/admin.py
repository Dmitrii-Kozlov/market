from django.contrib import admin
from .models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    list_display = ["__str__", "description", "price"]
    list_filter = ["price"]
    search_fields = ["title", "description"]
    list_editable = ["price"]
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
