from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

from products.models import Product
# Create your models here.

class TagManager(models.Manager):
    def all(self, *args, **kwargs):
        return super(TagManager, self).all(*args, **kwargs).filter(active=True)

class Tag(models.Model):
    title = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(unique=True)
    products = models.ManyToManyField(Product, blank=True)
    active = models.BooleanField(default=True)

    objects = TagManager()

    def __str__(self):
        return str(self.title)

    def get_absolute_url(self):
        view_name = "tags:detail"
        return reverse(view_name, kwargs={"slug": self.slug})

def tag_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance)


pre_save.connect(tag_pre_save_receiver, sender=Tag)