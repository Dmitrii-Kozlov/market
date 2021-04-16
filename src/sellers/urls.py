from django.urls import path, include
from .views import SellerDashboard, SellerTransactionListView, SellerProductDetailRedirectView
from products.views import ProductCreateView, SellerProductListView, ProductUpdateView
app_name = 'sellers'
urlpatterns = [
    path('', SellerDashboard.as_view(), name='dashboard'),
    path('transactions/', SellerTransactionListView.as_view(), name='transactions'),
    path('products/', SellerProductListView.as_view(), name='product_list'),
    path('product/<slug:slug>/', SellerProductDetailRedirectView.as_view()),
    path('product/<slug:slug>/edit/', ProductUpdateView.as_view(), name='product_update'),
    path('products/add/', ProductCreateView.as_view(), name='product_create'),
]