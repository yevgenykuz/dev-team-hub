from django.urls import path

from . import views

urlpatterns = [
    path('', views.wiki, name='wiki'),
    path('<slug:entry_slug>', views.entry, name='wiki_entry'),
    path('<slug:entry_slug>/add-favorite', views.add_entry_as_favorite, name='add_wiki_entry_as_favorite'),
    path('<slug:entry_slug>/remove-favorite', views.remove_entry_as_favorite, name='remove_wiki_entry_as_favorite')
]
