from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.utils.text import slugify


class Product(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)

    def __str__(self):
        return self.title

def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.title)
pre_save.connect(product_pre_save_reciever, sender=Product)