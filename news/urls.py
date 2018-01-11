from django.urls import path

from . import views

urlpatterns = [
    path('', views.NewsListView.as_view(), name='news'),
    path('tags/<str:tag>', views.articles_by_tag, name='articles_by_tag'),
    path('articles/<slug:article_slug>', views.article, name='article')
]
