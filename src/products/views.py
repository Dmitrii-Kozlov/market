from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .models import Product
from .forms import ProductAddForm, ProductModelForm
# Create your views here.

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'update_view.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('products:list')

    def get_object(self, queryset=None):
        user = self.request.user
        obj = super(ProductUpdateView, self).get_object()
        if obj.user == user or user in obj.managers.all():
            return obj
        else:
            raise Http404

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    template_name = 'create_view.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('products:list')

    def form_valid(self, form):
        user = self.request.user
        form.instance.user = user
        valid_data = super(ProductCreateView, self).form_valid(form)
        form.instance.managers.add(user)
        return valid_data

class ProductDetailView(DetailView):
    model = Product

class ProductListView(ListView):
    model = Product

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