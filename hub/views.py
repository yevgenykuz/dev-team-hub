import logging

from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, SearchRank, SearchQuery
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView

from forum.models import Post
from news.models import Article
from wiki.models import Entry
from .forms import SignUpForm

log = logging.getLogger(__name__)


def index(request):
    return render(request, "hub/index.html")


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'hub/accounts/signup.html', {'form': form})


@method_decorator(login_required, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = ('first_name', 'last_name', 'email',)
    template_name = 'hub/accounts/account.html'
    success_url = reverse_lazy('index')

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorite_wiki_entries'] = Entry.objects.filter(favorite_by__exact=self.request.user)
        context['my_posts'] = Post.objects.filter(updated_by__exact=self.request.user)
        context.update(self.kwargs)
        return context


def search(request):
    news_articles = None
    wiki_entries = None
    forum_posts = None
    if request.method == 'GET':
        text_query = request.GET.get('search_q', None)
        log.info(f"Search triggered for '{text_query}'")
        if text_query is not None:
            query = SearchQuery(text_query)

            # In what fields should we search? Give them weights (A highest)
            news_search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B') + SearchVector(
                'tags__name', weight='C')
            wiki_search_vector = SearchVector('name', weight='A') + SearchVector('value', weight='B') + SearchVector(
                'custom_fields__name', weight='C') + SearchVector('section__name', weight='D')
            forum_search_vector = SearchVector('body', weight='A') + SearchVector('topic__subject',
                                                                                  weight='B') + SearchVector(
                'topic__category__name', weight='C')

            # Custom weights [D,C,B,A]:
            news_weights = [0.3, 0.6, 0.8, 1.0]
            wiki_weights = [0.3, 0.5, 0.8, 1.0]
            forum_weights = [0.2, 0.3, 0.8, 1.0]

            # Run search and sort results by rank:
            news_ranked_results = SearchRank(news_search_vector, query, weights=news_weights)
            news_articles = Article.objects.annotate(rank=news_ranked_results).filter(
                rank__gte=0.2, publish__exact=True).distinct().order_by('-rank')
            wiki_ranked_results = SearchRank(wiki_search_vector, query, weights=wiki_weights)
            wiki_entries = Entry.objects.annotate(rank=wiki_ranked_results).filter(
                rank__gte=0.2, publish__exact=True).distinct().order_by('-rank')
            forum_ranked_results = SearchRank(forum_search_vector, query, weights=forum_weights)
            forum_posts = Post.objects.annotate(rank=forum_ranked_results).filter(
                rank__gte=0.2).distinct().order_by('-rank')

            if not news_articles and not wiki_entries and not forum_posts:
                log.warning(f"Search found nothing for '{text_query}'")

    return render(request, 'hub/search.html',
                  {'news_articles': news_articles, 'wiki_entries': wiki_entries, 'forum_posts': forum_posts})
