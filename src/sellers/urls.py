from django.urls import path, include
from .views import SellerDashboard
app_name = 'sellers'
urlpatterns = [
    path('', SellerDashboard.as_view(), name='dashboard'),
]