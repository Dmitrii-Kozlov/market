from django.shortcuts import render, get_object_or_404
from .models import Product
from .forms import ProductAddForm
# Create your views here.

def create_view(request):
    form = ProductAddForm(request.POST or None)
    if form.is_valid():
        form_data = form.cleaned_data
        new_obj = Product.objects.create(title=form_data.get('title'),
                                         description=form_data.get('description'),
                                         price=form_data.get('price'))
    template = 'create_view.html'
    context = {'form':form}
    return render(request, template, context)

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