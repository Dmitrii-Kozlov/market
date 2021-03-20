from django.shortcuts import render, get_object_or_404
from .models import Product
# Create your views here.

def detail_view(request, slug):
    obj = get_object_or_404(Product, slug=slug)
    #obj = Product.objects.get(pk=id)
    template = 'detail_view.html'
    context = {'obj':obj}
    return render(request, template, context)

def list_view(request):
    obj = Product.objects.all()
    template = 'list_view.html'
    context = {'obj':obj}
    return render(request, template, context)