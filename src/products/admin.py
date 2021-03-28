from django.contrib import admin
from .models import Product, MyProducts, Thumbnail
# Register your models here.

class ThumbnailInline(admin.TabularInline):
    model = Thumbnail

class ProductAdmin(admin.ModelAdmin):
    inlines = [ThumbnailInline]
    list_display = ["__str__", "description", "price", "user"]
    list_filter = ["price"]
    search_fields = ["title", "description"]
    list_editable = ["price"]
    prepopulated_fields = {'slug': ('title',), }
    class Meta:
        model = Product

admin.site.register(Product, ProductAdmin)
admin.site.register(MyProducts)
admin.site.register(Thumbnail)