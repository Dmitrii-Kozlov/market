import datetime

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum

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

    def get_transactions_today(self):
        today = datetime.date.today()
        today_min = datetime.datetime.combine(today, datetime.time.min)
        today_max = datetime.datetime.combine(today, datetime.time.max)
        return self.get_transaction().filter(timestamp__range=(today_min, today_max))

    def get_total_sales(self):
        total = self.get_transaction().aggregate(Sum("price"))
        return total["price__sum"]

    def get_today_sales(self):
        total = self.get_transactions_today().aggregate(Sum("price"))
        return total["price__sum"]
