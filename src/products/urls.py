from django.urls import path, include
from .views import (detail_view, list_view, create_view, update_view,
                    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView)
urlpatterns = [
    #path('<int:id>/', detail_view, name='detail_view'),
    path('list/', ProductListView.as_view(), name='product_list_view'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail_view'),
    path('product/<slug:slug>/edit/', ProductUpdateView.as_view(), name='product_update_view'),
    path('add/', ProductCreateView.as_view(), name='product_create_view'),


    path('create/',create_view, name='create_view'),
    path('<slug:slug>/edit/', update_view, name='update_view'),
    path('<slug:slug>/', detail_view, name='detail_view'),
    path('',list_view, name='list_view'),

]
