from django.contrib import admin
from .models import Tag
# Register your models here.

#admin.site.register(Tag)
@admin.register(Tag)
class TagModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Tag
    prepopulated_fields = {'slug': ('title',)}