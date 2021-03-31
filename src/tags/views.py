from django.shortcuts import render
from django.views.generic import DetailView, ListView

from .models import Tag
# Create your views here.

class TagDetailView(DetailView):
    model = Tag


class TagListView(ListView):
    model = Tag

    # def get_queryset(self):
    #     return Tag.objects.filter(active=True)

