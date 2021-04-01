import random

from django.shortcuts import render
from products.models import Product
# Create your views here.
# from django.views.generic.base import View
from django.views import View


class DashboardView(View):
    def get(self, request, *args, **kwargs):
        tag_view = None
        top_tags = None
        products = None
        try:
            tag_view = request.user.tagview_set.all().order_by("-count")[:5]
        except:
            pass
        owned = None
        try:
            owned = self.request.user.myproducts.products.all()
        except:
            pass
        if tag_view:
            top_tags = [x.tag for x in tag_view]
            products = Product.objects.filter(tag__in=top_tags)
            if owned:
                products = products.exclude(pk__in=owned)
            products = products.distinct()
            products = sorted(products, key=lambda x: random.random())
        context = {
            'products': products,
            'top_tags': top_tags
        }
        return render(request, 'dashboard/view.html', context)