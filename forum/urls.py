from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='forum'),
]
