from django import template
from ..models import Product, THUMB_CHOICES
register = template.Library()

@register.filter
def get_thumbnail(obj, arg):
    arg = arg.lower()
    if not isinstance(obj, Product):
        raise TypeError(f"{obj} is not valid for this model")
    choises = dict(THUMB_CHOICES)
    if not choises.get(arg):
        raise TypeError(f"{arg} is not valid type for this model")
    try:
        return obj.thumbnail_set.filter(type=arg).first().media.url
    except:
        return None
