from django.urls import path

from . import views

urlpatterns = [
    path('', views.wiki, name='wiki'),
    path('<slug:entry_slug>', views.entry, name='wiki_entry'),
]
