from django.urls import path

from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news'),
    path('tags/<tag>', views.NewsListView.as_view(), name='articles_by_tag'),
    path('articles/<slug:article_slug>', views.article, name='article')
]
