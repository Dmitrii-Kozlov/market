import os
from mimetypes import guess_type
from wsgiref.util import FileWrapper

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from analytics.models import TagView
from .models import Product
from tags.models import Tag
from .forms import ProductAddForm, ProductModelForm
# Create your views here.

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    template_name = 'update_view.html'
    form_class = ProductModelForm
    success_url = reverse_lazy('products:list')

    def get_initial(self):
        initial = super(ProductUpdateView, self).get_initial()
        tags = self.get_object().tag_set.all()
        initial['tags'] = ', '.join([x.title for x in tags])
        return initial

    def get_object(self, queryset=None):
        user = self.request.user
        obj = super(ProductUpdateView, self).get_object()
        if obj.user == user or user in obj.managers.all():
            return obj
        else:
            raise Http404

    def form_valid(self, form):
        valid_data = super(ProductUpdateView, self).form_valid(form)
        print(form.cleaned_data)
        tags = form.cleaned_data.get('tags')
        obj = self.get_object()
        obj.tag_set.clear()
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                if tag != "":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(self.get_object())
        return valid_data

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
        tags = form.cleaned_data.get('tags')
        if tags:
            tag_list = tags.split(',')
            for tag in tag_list:
                if tag != "":
                    new_tag = Tag.objects.get_or_create(title=str(tag).strip())[0]
                    new_tag.products.add(form.instance)
        return valid_data

class ProductDetailView(DetailView):
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        tags = obj.tag_set.all()
        for tag in tags:
            TagView.objects.add_count(user=self.request.user, tag=tag)
        return context

class ProductDownloadView(DetailView):
    model = Product
    def get(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj in request.user.myproducts.products.all():
            filepath = os.path.join(settings.PROTECTED_ROOT, obj.media.path)
            guessed_type = guess_type(filepath)[0]
            wrapper = FileWrapper(open(filepath, 'rb'))
            # mimetype = 'application/force-download'
            # if guessed_type:
            #     mimetype = guessed_type
            mimetype = guessed_type if guessed_type else 'application/force-download'
            responce = HttpResponse(wrapper, content_type=mimetype)
            if not request.GET.get('preview'):
                responce["Content-Disposition"] = f"attachment; filename={obj.media.name}"
            #responce["Content-Disposition"] = f"attachment; filename={obj.media.name}"
            responce["X-SendFile"] = str(obj.media.name)
            return responce
        else:
            raise Http404



class ProductListView(ListView):
    model = Product
    def get_queryset(self):
        qs = super(ProductListView, self).get_queryset()
        query = self.request.GET.get('q')
        if query:
            qs = qs.filter(
                Q(title__icontains = query)|
                Q(description__icontains = query)
            )
        return qs


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