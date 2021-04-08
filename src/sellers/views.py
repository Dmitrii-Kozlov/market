from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic.edit import FormMixin

from .forms import NewSellerForm
from .models import SellerAccount

class SellerDashboard(LoginRequiredMixin, FormMixin, View):
    form_class = NewSellerForm
    success_url = "/seller/"

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def get(self, request, *args, **kwargs):
        apply_form = self.get_form()
        account = SellerAccount.objects.filter(user=self.request.user)
        exists = account.exists()
        active = None
        # context = {
        #     'apply_form': apply_form,
        #     'account': account,
        #     'active': active,
        #     'exists': exists
        # }
        context = {}
        if exists:
            account = account.first()
            active = account.active
        if not exists and not active:
            context["title"] = "Apply this form"
            context["apply_form"] = apply_form
        elif exists and not active:
            context["title"] = "Account Pending"
        elif exists and active:
            context["title"] = "Seller Dashboard"

        return render(request, "sellers/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data