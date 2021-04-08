from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View
from .forms import NewSellerForm

class SellerDashboard(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = NewSellerForm(request.POST)
        if form.is_valid():
            print("add new seller")
        return render(request, "sellers/dashboard.html", {'form': form})

    def get(self, request, *args, **kwargs):
        form = NewSellerForm()
        return render(request, "sellers/dashboard.html", {'form': form})