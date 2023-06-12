from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView

from .models import Article, Tag


class NewsListView(ListView):
    model = Article
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_list'] = Tag.objects.all()
        context.update(self.kwargs)
        return context

    def get_queryset(self):
        try:
            return Article.objects.filter(publish__exact=True, tags__name__exact=self.kwargs['tag'])
        except KeyError:
            return Article.objects.filter(publish__exact=True)


@require_http_methods(["GET"])
def article(request, article_slug):
    # get article_slug parameter to render the needed article
    returned_article = get_object_or_404(Article, slug=article_slug)
    return render(request, 'news/article.html', {'article': returned_article})
