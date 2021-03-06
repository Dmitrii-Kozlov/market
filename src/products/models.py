from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import pre_save, post_save
from django.urls import reverse
from django.utils.text import slugify

from sellers.models import SellerAccount


def download_media_location(instance, filename):
    return f"{instance.slug}/{filename}"


class Product(models.Model):
    seller = models.ForeignKey(SellerAccount, on_delete=models.CASCADE)
    # user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # managers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="managers_products", blank=True)
    media = models.ImageField(blank=True,
                              null=True,
                              upload_to=download_media_location,
                              storage=FileSystemStorage(location=settings.PROTECTED_ROOT))
    title = models.CharField(max_length=30)
    slug = models.SlugField(blank=True, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=100, decimal_places=2, default=9.99, null=True, )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        view_name = "products:detail"
        return reverse(view_name, kwargs={"slug": self.slug})

    def get_edit_url(self):
        view_name = "sellers:product_update"
        return reverse(view_name, kwargs={"slug": self.slug})

    def get_download(self):
        view_name = "products:download"
        url = reverse(view_name, kwargs={"slug": self.slug})
        return url


def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Product.objects.filter(slug=slug)
    exists = qs.exists()
    if exists:
        new_slug = f'{slug}-{qs.first().id}'
        return create_slug(instance, new_slug=new_slug)
    return slug


def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)


pre_save.connect(product_pre_save_receiver, sender=Product)


def thumbnail_location(instance, filename):
    return f"{instance.product.slug}/{filename}"


THUMB_CHOICES = (
    ("hd", "HD"),
    ("sd", "SD"),
    ("micro", "Micro"),
)


class Thumbnail(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    type = models.CharField(max_length=20, choices=THUMB_CHOICES, default='hd')
    height = models.CharField(max_length=20, null=True, blank=True)
    width = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(
        width_field="width",
        height_field="height",
        blank=True,
        null=True,
        upload_to=thumbnail_location)

    def __str__(self):
        return str(self.media.path)


import os
import shutil
from PIL import Image
import random

from django.core.files import File

def create_thumb(media_path, instance, owner_slug, max_length, max_width):
    filename = os.path.basename(media_path)
    thumb = Image.open(media_path)
    size = (max_length, max_width)
    thumb.thumbnail(size, Image.ANTIALIAS)
    temp_loc = os.path.join(settings.MEDIA_ROOT, owner_slug, 'tmp')
    if not os.path.exists(temp_loc):
        os.makedirs(temp_loc)
    temp_file_path = os.path.join(temp_loc, filename)
    if os.path.exists(temp_file_path):
        temp_path = os.path.join(temp_loc, f"{random.random()}")
        os.makedirs(temp_path)
        temp_file_path = os.path.join(temp_path, filename)

    temp_image = open(temp_file_path, "wb")
    thumb.save(temp_image)
    thumb_data = open(temp_file_path, "rb")

    thumb_file = File(thumb_data)
    instance.media.save(filename, thumb_file)
    shutil.rmtree(temp_loc, ignore_errors=True)
    return True

def product_post_save_receiver(sender, instance, created, *args, **kwargs):
    if instance.media:
        hd, hd_created = Thumbnail.objects.get_or_create(product=instance, type='hd')
        sd, sd_created = Thumbnail.objects.get_or_create(product=instance, type='sd')
        micro, micro_created = Thumbnail.objects.get_or_create(product=instance, type='micro')

        hd_max = (400, 400)
        sd_max = (200, 200)
        micro_max = (50, 50)
        media_path = instance.media.path
        owner_slug = instance.slug
        if hd_created:
            create_thumb(media_path, hd, owner_slug, *hd_max)
            #
            # filename = os.path.basename(instance.media.path)
            # thumb = Image.open(instance.media.path)
            # thumb.thumbnail(hd_max, Image.ANTIALIAS)
            # temp_loc = os.path.join(settings.MEDIA_ROOT, instance.slug, 'tmp')
            # if not os.path.exists(temp_loc):
            #     os.makedirs(temp_loc)
            # temp_file_path = os.path.join(temp_loc, filename)
            # if os.path.exists(temp_file_path):
            #     temp_path = os.path.join(temp_loc, f"{random.random()}")
            #     os.makedirs(temp_path)
            #     temp_file_path = os.path.join(temp_path, filename)
            #
            # temp_image = open(temp_file_path, "wb")
            # thumb.save(temp_image)
            # thumb_data = open(temp_file_path, "rb")
            #
            # thumb_file = File(thumb_data)
            # hd.media.save(filename, thumb_file)

        if sd_created:
            create_thumb(media_path, sd, owner_slug, *sd_max)

        if micro_created:
            create_thumb(media_path, micro, owner_slug, *micro_max)

    # shutil.rmtree(temp_loc, ignore_errors=True)


post_save.connect(product_post_save_receiver, sender=Product)


class MyProducts(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f"{self.products.count()}"

    class Meta:
        verbose_name = "My Products"
        verbose_name_plural = "My Products"

class ProductRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(null=True, blank=True)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.rating}"
