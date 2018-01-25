from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import UpdateView
from forum.models import Post
from news.models import Article
from wiki.models import Entry

from .forms import SignUpForm


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
        if text_query is not None:
            query = SearchQuery(text_query)
            news_search_vector = SearchVector('title', weight='A') + SearchVector('body', weight='B') + SearchVector(
                'tags__name', weight='C')
            wiki_search_vector = SearchVector('name', weight='A') + SearchVector('value', weight='B') + SearchVector(
                'custom_fields__name', weight='C')
            forum_search_vector = SearchVector('topic__subject', weight='A') + SearchVector('body', weight='B')

            news_articles = Article.objects.annotate(rank=SearchRank(news_search_vector, query)).filter(
                rank__gte=0.3, published__exact=True).order_by('-rank')
            wiki_entries = Entry.objects.annotate(rank=SearchRank(wiki_search_vector, query)).filter(
                rank__gte=0.3, published__exact=True).order_by('-rank')
            forum_posts = Post.objects.annotate(rank=SearchRank(forum_search_vector, query)).filter(
                rank__gte=0.3).order_by('-rank')

    return render(request, 'hub/search.html',
                  {'news_articles': news_articles, 'wiki_entries': wiki_entries, 'forum_posts': forum_posts})
