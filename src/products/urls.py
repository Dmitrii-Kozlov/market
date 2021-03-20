from django.urls import path, include
from .views import detail_view, list_view
urlpatterns = [
    #path('<int:id>/', detail_view, name='detail_view'),
    path('<slug:slug>/', detail_view, name='detail_view'),
    path('',list_view, name='list_view')

]
