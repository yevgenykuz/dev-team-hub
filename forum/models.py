import math

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse

# Used for pagination in views and calculations here:
PAGE_LIMIT = 8


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, editable=False)
    description = models.CharField(max_length=1000, help_text="What kind of topics should be in this category?")
    order_id = models.PositiveSmallIntegerField(default=0,
                                                help_text="The presentation order in the forum category list, relative"
                                                          " to other forum categories.")

    class Meta:
        ordering = ["order_id"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # update slug field when saving:
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("topics_of_category", args=[self.slug])

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

    def get_absolute_url(self):
        return reverse("posts_of_topic", args=[self.category.slug, self.slug])

    def get_page_count(self):
        count = self.post_set.count()
        pages = count / PAGE_LIMIT
        return int(math.ceil(pages))

    def has_many_pages(self, count=None):
        if count is None:
            count = self.get_page_count()
        return count > 5

    def get_page_range(self):
        count = self.get_page_count()
        if self.has_many_pages(count):
            return range(1, 4)
        return range(1, count + 1)

    def get_last_posts(self, count=PAGE_LIMIT):
        return self.post_set.order_by('-last_updated')[:count]

    def get_last_post(self):
        return self.get_last_posts(count=1)[0]


class Post(models.Model):
    body = RichTextField(max_length=5000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["last_updated"]

    def __str__(self):
        return f"{self.body[:50]}..." if len(self.body) > 50 else self.body

    def get_absolute_url(self):
        topic_url = reverse('posts_of_topic',
                            kwargs={'category_slug': self.topic.category.slug,
                                    'topic_slug': self.topic.slug})
        post_location = 1
        posts = self.topic.post_set.all()
        for post in posts:
            if post.pk is self.pk:
                break
            post_location += 1
        return f"{topic_url}?page={math.ceil(post_location / PAGE_LIMIT)}#{self.pk}"
