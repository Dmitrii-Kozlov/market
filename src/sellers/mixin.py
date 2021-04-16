from django.contrib.auth.mixins import LoginRequiredMixin

from billing.models import Transaction
from products.models import Product
from .models import SellerAccount

class SellerAccounMixin(LoginRequiredMixin, object):
    account = None
    products = []
    transactions = []

    def get_account(self):
        user = self.request.user
        accounts = SellerAccount.objects.filter(user=user)
        if accounts.exists() and accounts.count() == 1:
            self.account = accounts.first()
            return accounts.first()
        return None

    def get_products(self):
        account = self.get_account()
        products = Product.objects.filter(seller=account)
        self.products = products
        return products

    def get_transaction(self):
        products = self.get_products()
        transactions = Transaction.objects.filter(product__in=products)
        self.transactions = transactions
        return transactions

