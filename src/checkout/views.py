import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, Http404
from django.views import View
from digitalmarket.mixins import AjaxRequiredMixin
from products.models import Product, MyProducts

class CheckoutAjaxView(AjaxRequiredMixin, View):
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({}, status=401)
        user = request.user
        product_id = request.POST.get("product_id")
        exist = Product.objects.filter(id=product_id).exists()
        if not exist:
            return JsonResponse({}, status=404)
        try:
            product_obj = Product.objects.get(id=product_id)
        except:
            product_obj = Product.objects.filter(id=product_id).first()
        my_products = MyProducts.objects.get_or_create(user=user)[0]
        my_products.products.add(product_obj)
        data = {
            "works": True,
            "time": datetime.datetime.now()
        }
        return JsonResponse(data)


class CheckoutTestView(View):
    def post(self, requset):
        if requset.is_ajax():
            if not requset.user.is_authenticated():
                data = {
                    "works": False,
                }
                return JsonResponse(data, status=401)
            data = {
                "works": True,
                "time": datetime.datetime.now()
            }
            return JsonResponse(data)
        return HttpResponse("Hello there!")
    def get(self, request):
        # <view logic>
        context = {}
        template = 'checkout/test.html'
        return render(request, template, context)
