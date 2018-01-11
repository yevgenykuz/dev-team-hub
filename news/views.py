from django.http import HttpResponse
from django.views.generic import ListView

from .models import Article


class NewsListView(ListView):
    model = Article


def articles_by_tag(request, tag):
    # get tag parameter to render list of all articles with this tag, ordered by latest date
    return HttpResponse("News -> tags -> {}".format(tag))


def article(request, article_slug):
    # get article_slug parameter to render the needed article
    return HttpResponse("News -> articles -> {}".format(article_slug))
