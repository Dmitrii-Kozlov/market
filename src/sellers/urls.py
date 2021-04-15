from django.urls import path, include
from .views import SellerDashboard, SellerTransactionListView
app_name = 'sellers'
urlpatterns = [
    path('', SellerDashboard.as_view(), name='dashboard'),
    path('transactions/', SellerTransactionListView.as_view(), name='transactions')
]