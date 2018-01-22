from django.urls import path

from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='forum'),
    path('<slug:category_slug>', views.TopicListView.as_view(), name='topics_of_category'),
    path('<slug:category_slug>/new_topic', views.new_topic, name='new_topic'),
    path('<slug:category_slug>/<slug:topic_slug>', views.PostListView.as_view(), name='posts_of_topic'),
    path('<slug:category_slug>/<slug:topic_slug>/reply', views.reply_topic, name='reply_topic'),
    path('<slug:category_slug>/<slug:topic_slug>/<int:post_pk>/edit', views.PostUpdateView.as_view(), name='edit_post'),
]
