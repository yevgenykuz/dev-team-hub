from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class CustomFieldType(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="A custom field type")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    name_plural = models.CharField(max_length=255, help_text="This type in plural, for wiki entry presentation")
    description = models.TextField(max_length=2500, help_text="Describe this custom field type")
    order_id = models.PositiveSmallIntegerField(default=0, help_text="Order in wiki entry page")

    class Meta:
        ordering = ["order_id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = slugify(self.name)
        super(CustomFieldType, self).save(*args, **kwargs)


class CustomField(models.Model):
    name = models.CharField(max_length=200, help_text="A custom field")
    type = models.ForeignKey(CustomFieldType, on_delete=models.SET_NULL, null=True, help_text="The type of this field")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    value = RichTextField(max_length=20000, help_text="The value of this field")
    order_id = models.PositiveSmallIntegerField(default=0, help_text="Order in wiki entry page")

    class Meta:
        ordering = ["type__slug", "order_id"]

    def __str__(self):
        return "[" + self.type.name + "] " + self.name

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = self.type.slug + "-" + slugify(self.name)
        super(CustomField, self).save(*args, **kwargs)


class Section(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="A wiki section/category")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField(max_length=2500, help_text="Describe this wiki section")
    order_id = models.PositiveSmallIntegerField(unique=True, default=0,
                                                help_text="Order in wiki sections menu")

    class Meta:
        ordering = ["order_id"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = slugify(self.name)
        super(Section, self).save(*args, **kwargs)


class Entry(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True,
                                help_text="The section to witch this entry belongs")
    name = models.CharField(max_length=200, unique=True, help_text="A wiki entry")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    published = models.BooleanField(default=False)
    value = RichTextField(max_length=20000, help_text="The value of this field", blank=True)
    custom_fields_presentation_order = models.ManyToManyField(CustomFieldType, blank=True,
                                                              help_text="The custom field types (if any)."
                                                                        " The presentation order (that's determined by"
                                                                        " the order_id of the type) will be shown on"
                                                                        "the right after saving")
    custom_fields = models.ManyToManyField(CustomField, blank=True,
                                           help_text="The custom fields (if any), "
                                                     "The presentation order (that's determined by"
                                                     " the order_id of the field) will be shown on"
                                                     "the right after saving")
    favorite_by = models.ManyToManyField(User, blank=True,
                                         help_text="A list of users that marked this entry as their favorite,"
                                                   " better leave untouched")
    order_id = models.PositiveSmallIntegerField(default=0, help_text="Order in wiki section page")

    class Meta:
        ordering = ["section__slug", "order_id"]
        verbose_name_plural = "entries"

    def __str__(self):
        return "[" + self.section.name + "] " + self.name

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = self.section.slug + "-" + slugify(self.name)
        super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        # the url of an entry is represented by the entry slug:
        return reverse("wiki_entry", args=[self.slug])
