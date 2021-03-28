from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils.text import slugify

def download_media_location(instance, filename):
    return f'{instance.slug}/{filename}'

class Product(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    media = models.FileField(blank=True, null=True,
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

def product_pre_save_reciever(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)
pre_save.connect(product_pre_save_reciever, sender=Product)

def thumbnail_location(instance, filename):
    return f'{instance.product.slug}/{filename}'

class Thumbnail(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    width = models.CharField(max_length=20, null=True, blank=True)
    height = models.CharField(max_length=20, null=True, blank=True)
    media = models.ImageField(blank=True, null=True,
                              width_field="width",
                              height_field="height",
                              upload_to=thumbnail_location,
                              )
    def __str__(self):
        return str(self.media.path)

class MyProducts(models.Model):
    class Meta:
        verbose_name_plural = 'MyProducts'
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, blank=True)

    def __str__(self):
        return f'{self.products.count()}'