import math

from ckeditor.fields import RichTextField
from ckeditor.widgets import CKEditorWidget
from django import forms
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, editable=False)
    description = models.CharField(max_length=1000, help_text="What kind of topics should be in this category?")

    class Meta:
        ordering = ["slug"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # update slug field when saving:
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_posts_count(self):
        return Post.objects.filter(topic__category=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__category=self).order_by('-last_updated').first()


class Topic(models.Model):
    subject = models.CharField(max_length=255)
    slug = models.SlugField(max_length=300, unique=True, editable=False)
    last_updated = models.DateTimeField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    views = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["last_updated"]

    def __str__(self):
        return self.subject

    def save(self, *args, **kwargs):
        # update slug field when saving:
        self.slug = slugify(self.subject) + '-' + str(self.pk)
        super(Topic, self).save(*args, **kwargs)

    def get_page_count(self):
        count = self.post_set.count()
        pages = count / 10
        return int(math.ceil(pages))

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 6

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 5)
        return range(1, count + 1)

    def get_last_ten_posts(self):
        return self.post_set.order_by('-last_updated')[:10]


class NewTopicForm(forms.ModelForm):
    body = forms.CharField(
        widget=CKEditorWidget(),
        max_length=5000,
        help_text='The max length of the text is 5000.'
    )

    class Meta:
        model = Topic
        fields = ['subject', 'body']


class Post(models.Model):
    body = RichTextField(max_length=5000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["last_updated"]

    def __str__(self):
        return (self.body[:50] + '...') if len(self.body) > 50 else self.body


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['body', ]
