from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

# Create your views here.
from django.views import View
from django.views.generic import ListView
from django.views.generic.edit import FormMixin

from .forms import NewSellerForm
from .models import SellerAccount
from products.models import Product
from billing.models import Transaction
from .mixin import SellerAccounMixin

from django.shortcuts import get_object_or_404
from django.views.generic.base import RedirectView

class SellerProductDetailRedirectView(RedirectView):
    permanent = True
    def get_redirect_url(self, *args, **kwargs):
        obj = get_object_or_404(Product, slug=kwargs['slug'])
        return obj.get_absolute_url()


class SellerTransactionListView(SellerAccounMixin, ListView):
    model = Transaction
    template_name = "sellers/transaction_list_view.html"

    def get_queryset(self):
        return self.get_transaction()
        # account = SellerAccount.objects.filter(user=self.request.user)
        # if account.exists():
        #     account = account.first()
        #     products = Product.objects.filter(seller=account)
        #     return Transaction.objects.filter(product__in=products)
        # return []

class SellerDashboard(SellerAccounMixin, FormMixin, View):
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
        account = self.get_account()
        exists = account
        active = None
        context = {}
        if account:
            active = account.active
        if not account and not active:
            context["title"] = "Apply this form"
            context["apply_form"] = apply_form
        elif account and not active:
            context["title"] = "Account Pending"
        elif account and active:
            context["title"] = "Seller Dashboard"
            # products = Product.objects.filter(seller=account)
            context["products"] = self.get_products()
            context["transactions"] = self.get_transaction()[:5]

        return render(request, "sellers/dashboard.html", context)

    def form_valid(self, form):
        valid_data = super(SellerDashboard, self).form_valid(form)
        obj = SellerAccount.objects.create(user=self.request.user)
        return valid_data