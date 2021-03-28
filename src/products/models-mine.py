from django.conf import settings
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify

def download_media_location(instance, filename):
    return f'{instance.slug}/{filename}'

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    media = models.ImageField(blank=True, null=True,
                             upload_to=download_media_location,
                             storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    managers = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name='managers_products')
    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('products:detail', kwargs={'slug': self.slug})

    def get_download(self):
        return reverse('products:download', kwargs={'slug': self.slug})

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exist = qs.exists()
    if exist:
        new_slug = f'{slug}-{qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug

def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(product_pre_save_receiver, sender=Product)


def thumbnail_location(instance, filename):
    return f'{instance.product.slug}/{filename}'

THUMB_CHOISES = (
    ("hd", "HD"),
    ("md", "MD"),
    ("micro", "Micro")
)

class Thumbnail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=THUMB_CHOISES, default='hd')
    width = models.CharField(max_length=20, null=True, blank=True)
    height = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(blank=True, null=True,
                              width_field="width",
                              height_field="height",
                              upload_to=thumbnail_location,
                              )
    def __str__(self):
        return str(self.media.path)

import os
import shutil
from PIL import Image
import random


def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.media:
        hd = Thumbnail.objects.get_or_create(product=instance, type='hd')[0]
        sd = Thumbnail.objects.get_or_create(product=instance, type='sd')[0]
        micro = Thumbnail.objects.get_or_create(product=instance, type='micro')[0]

        hd_max = (400, 400)
        sd_max = (200, 200)
        micro_max = (50, 50)

        filename = os.path.basename(instance.media.path)
        print(f'{filename=}')
        thumb = Image.open(instance.media.path)
        thumb.thumbnail(hd_max, Image.ANTIALIAS)
        temp_loc = os.path.join(settings.MEDIA_ROOT, instance.slug, 'tmp')
        if not os.path.exists(temp_loc):
            os.makedirs(temp_loc)
        print(f'{temp_loc=}')
        temp_file_path = os.path.join(temp_loc, filename)
        if os.path.exists(temp_file_path):
            temp_path = os.path.join(temp_loc, f'{random.random()}')
            os.makedirs(temp_path)
            temp_file_path = os.path.join(temp_path, filename)
        temp_image = open(temp_file_path, 'wb')
        thumb.save(temp_image)
        print('save image')
        temp_thumb = open(temp_file_path, 'rb')
        print('open image')
        thumb_file = File(temp_thumb)

        hd.media.save(filename, thumb_file)
        print('save hd media')
        #shutil.rmtree(temp_loc, ignore_errors=True)



post_save.connect(product_post_save_receiver, sender=Product)


class MyProducts(models.Model):
    class Meta:
        verbose_name_plural = 'MyProducts'
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f'{self.products.count()}'