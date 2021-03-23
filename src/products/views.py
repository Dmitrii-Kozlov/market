from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product
from .forms import ProductAddForm, ProductModelForm
# Create your views here.

class ProductUpdateView(UpdateView):
    model = Product
    template_name = 'update_view.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('product_list_view')

class ProductCreateView(CreateView):
    model = Product
    template_name = 'create_view.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('product_list_view')

    # def form_valid(self, form):
    #     try:
    #         form.save()
    #     except IntegrityError:
    #         self.instance = form.save(commit=False)
    #         self.instance.slug += '-n'
    #         #self.form_valid(self.instance)
    #         #self.instance.save()
    #         return super(ProductCreateView, self).form_valid(form)
    #     return super(ProductCreateView, self).form_valid(form)

class ProductDetailView(DetailView):
    model = Product

class ProductListView(ListView):
    model = Product
    #template_name = 'list_view.html'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['obj'] = self.get_queryset()
    #     return context

def create_view(request):
    if request.method == "POST":
        form = ProductModelForm(request.POST)
        if form.is_valid():
            try:
                form.save()
            except IntegrityError:
                instance = form.save(commit=False)
                instance.slug += '-n'
                instance.save()
        return redirect('list_view')
    else:
        form = ProductModelForm()
    # if form.is_valid():
    #     form_data = form.cleaned_data
    #     new_obj = Product.objects.create(title=form_data.get('title'),
    #                                      description=form_data.get('description'),
    #                                      price=form_data.get('price'))
    template = 'create_view.html'
    context = {'form':form}
    return render(request, template, context)

def update_view(request, slug):
    obj = get_object_or_404(Product, slug=slug)
    if request.method == 'POST':
        form = ProductModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
        return redirect('detail_view', slug=slug)
    else:
        form = ProductModelForm(instance=obj)
    template = 'update_view.html'
    context = {'form': form}
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