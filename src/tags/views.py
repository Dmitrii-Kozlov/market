from django.shortcuts import render
from django.views.generic import DetailView, ListView
from analytics.models import TagView
from .models import Tag
# Create your views here.

class TagDetailView(DetailView):
    model = Tag

    def get_context_data(self, **kwargs):
        context = super(TagDetailView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            analytic_obj = TagView.objects.get_or_create(user=self.request.user, tag=self.get_object())[0]
            analytic_obj.count += 1
            analytic_obj.save()
        return context



class TagListView(ListView):
    model = Tag

    # def get_queryset(self):
    #     return Tag.objects.filter(active=True)

