import datetime

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View


class CheckoutTestView(View):
    def post(self, requset):
        if requset.is_ajax():
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
