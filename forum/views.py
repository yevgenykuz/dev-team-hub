from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, UpdateView

from forum.forms import NewTopicForm, PostForm
from .models import Category, Topic, Post, PAGE_LIMIT


class CategoryListView(ListView):
    model = Category


class TopicListView(ListView):
    model = Topic
    paginate_by = PAGE_LIMIT

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

    def get_queryset(self):
        category = get_object_or_404(Category, slug=self.kwargs.get('category_slug'))
        queryset = category.topic_set.order_by('-last_updated').annotate(replies=Count('post') - 1)
        # noinspection PyAttributeOutsideInit
        self.category = category
        return queryset


class PostListView(ListView):
    model = Post
    paginate_by = PAGE_LIMIT

    def get_context_data(self, **kwargs):
        # use sessions to prevent the same user refreshing the page counting as multiple views:
        session_key = 'viewed_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        context = super().get_context_data(**kwargs)
        context['topic'] = self.topic
        return context

    def get_queryset(self):
        topic = get_object_or_404(Topic, category__slug=self.kwargs.get('category_slug'),
                                  slug=self.kwargs.get('topic_slug'))
        queryset = topic.post_set.order_by('last_updated')
        # noinspection PyAttributeOutsideInit
        self.topic = topic
        return queryset


@login_required
@require_http_methods(["GET", "POST"])
def new_topic(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if request.method == 'POST':
        form = NewTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.category = category
            topic.created_by = request.user
            topic.save()
            Post.objects.create(
                body=form.cleaned_data.get('body'),
                topic=topic,
                updated_by=request.user
            )
            return redirect('posts_of_topic', category_slug=category_slug, topic_slug=topic.slug)
    else:
        form = NewTopicForm()
    return render(request, 'forum/new_topic.html', {'category': category, 'form': form})


@login_required
@require_http_methods(["GET", "POST"])
def reply_topic(request, category_slug, topic_slug):
    topic = get_object_or_404(Topic, category__slug=category_slug, slug=topic_slug)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.updated_by = request.user
            post.save()

            topic.last_updated = timezone.now()
            topic.save()

            topic_url = reverse('posts_of_topic', kwargs={'category_slug': category_slug, 'topic_slug': topic_slug})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
            )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request, 'forum/reply_topic.html', {'topic': topic, 'form': form})


@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('body',)
    template_name = 'forum/edit_post.html'
    pk_url_kwarg = 'post_pk'

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(updated_by=self.request.user)

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updated_by = self.request.user
        post.last_updated = timezone.now()
        post.save()
        return redirect('posts_of_topic', category_slug=post.topic.category.slug, topic_slug=post.topic.slug)
