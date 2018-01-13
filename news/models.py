import datetime

from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="A tag for news articles")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        # the url of an article is represented by its slug:
        return reverse("articles_by_tag", args=[self.name])


class Article(models.Model):
    title = models.CharField(max_length=200, help_text="Article title")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    published = models.BooleanField(default=False)
    body = RichTextField(max_length=20000, help_text="Write the article here")
    tags = models.ManyToManyField(Tag, blank=True, help_text="Add tags that describe this article")

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = slugify(self.title) + '-' + str(datetime.date.today())
        super(Article, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # the url of an article is represented by its slug:
        return reverse("article", args=[self.slug])

    def display_tags(self):
        """
        Used by the admin page to add the tags of an article to the articles list
        :return: a string representation of the tags of an article
        """
        return ", ".join([tag.name for tag in self.tags.all()])

    # this is the title of the admin page column that holds the display_tags() data
    display_tags.short_description = "Tags"
