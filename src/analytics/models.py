from django.db import models
from django.conf import settings
from tags.models import Tag

# Create your models here.

class TagView(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)

    def __str__(self):
        return str(self.tag.title)