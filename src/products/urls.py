from django.urls import path, include
from .views import detail_view, list_view, create_view, update_view
urlpatterns = [
    #path('<int:id>/', detail_view, name='detail_view'),
    path('create/',create_view, name='create_view'),
    path('<slug:slug>/edit/', update_view, name='update_view'),
    path('<slug:slug>/', detail_view, name='detail_view'),
    path('',list_view, name='list_view')

]
