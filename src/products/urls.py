from django.urls import path, include
from .views import (detail_view, list_view, create_view, update_view,
                    ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDownloadView)
app_name = 'products'
urlpatterns = [
    #path('<int:id>/', detail_view, name='detail_view'),
    path('', ProductListView.as_view(), name='list'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='detail'),
    path('product/<slug:slug>/edit/', ProductUpdateView.as_view(), name='update'),
    path('product/<slug:slug>/download/', ProductDownloadView.as_view(), name='download'),
    path('add/', ProductCreateView.as_view(), name='create'),

    #
    # path('create/',create_view, name='create_view'),
    # path('<slug:slug>/edit/', update_view, name='update_view'),
    # path('<slug:slug>/', detail_view, name='detail_view'),
    # path('',list_view, name='list_view'),

]
