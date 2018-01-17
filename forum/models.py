from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=60, unique=True, editable=False)
    description = models.CharField(max_length=1000)

    class Meta:
        ordering = ["slug"]
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


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
        # update slug field when saving - subject-pk:
        self.slug = slugify(self.subject) + '-' + self.pk
        super(Topic, self).save(*args, **kwargs)


class Post(models.Model):
    body = RichTextField(max_length=5000)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now_add=True)
    updated_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ["last_updated"]

    def __str__(self):
        return (self.body[:50] + '...') if len(self.body) > 50 else self.body
