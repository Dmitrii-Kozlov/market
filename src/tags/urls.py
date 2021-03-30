from django.urls import path, include
from .views import TagDetailView, TagListView

app_name = 'tags'
urlpatterns = [
    path('', TagListView.as_view(), name='list'),
    path('<slug:slug>/', TagDetailView.as_view(), name='detail'),
]
