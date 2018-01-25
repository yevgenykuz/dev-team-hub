"""
dev-team-hub URL Configuration
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('hub.urls')),
    path('news/', include('news.urls')),
    path('wiki/', include('wiki.urls')),
    path('forum/', include('forum.urls')),
    path('admin/', admin.site.urls),
]
