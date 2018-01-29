from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.text import slugify


class CustomFieldType(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="A meaningful name.")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    name_plural = models.CharField(max_length=255,
                                   help_text="The title of the 'block' in the wiki entry page that holds fields of"
                                             " this custom type.")
    description = models.TextField(max_length=2500, help_text="How should custom fields of this type look like?")
    order_id = models.PositiveSmallIntegerField(default=0,
                                                help_text="The presentation order of this custom field type 'block' in"
                                                          " a wiki entry page, relative to other custom field type"
                                                          " 'blocks'.")

    class Meta:
        ordering = ["order_id", "slug"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = slugify(self.name)
        super(CustomFieldType, self).save(*args, **kwargs)


class CustomField(models.Model):
    name = models.CharField(max_length=200, help_text="The key/title/name of an actual field.")
    type = models.ForeignKey(CustomFieldType, on_delete=models.SET_NULL, null=True, help_text="The type of this field.")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    value = RichTextField(max_length=20000, help_text="The value/body/textual data of this field.")
    order_id = models.PositiveSmallIntegerField(default=0,
                                                help_text="The presentation order of this field in the 'block' that"
                                                          " holds field of this type on a wiki page, relative to other"
                                                          " fields of the same type.")

    class Meta:
        ordering = ["type__order_id", "order_id", "slug"]

    def __str__(self):
        return f"{self.type.name} {self.name}"

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = self.type.slug + "-" + slugify(self.name)
        super(CustomField, self).save(*args, **kwargs)


class Section(models.Model):
    name = models.CharField(max_length=200, unique=True, help_text="The name of a wiki section/category.")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    description = models.TextField(max_length=2500, help_text="What entries should this wiki section hold?")
    order_id = models.PositiveSmallIntegerField(default=0,
                                                help_text="The presentation order in the wiki sections menu, relative"
                                                          " to other wiki sections.")

    class Meta:
        ordering = ["order_id", "slug"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = slugify(self.name)
        super(Section, self).save(*args, **kwargs)

    def get_absolute_url(self):
        wiki_url = reverse("wiki")
        wiki_sections = Section.objects.all()
        section_location = 0
        for section in wiki_sections:
            if section.pk is self.pk:
                break
            section_location += 1
        return f"{wiki_url}?slide={section_location}"


class Entry(models.Model):
    section = models.ForeignKey(Section, on_delete=models.SET_NULL, null=True,
                                help_text="The wiki section to which this entry belongs.")
    name = models.CharField(max_length=200, unique=True, help_text="The title of this wiki entry (page).")
    slug = models.SlugField(max_length=255, unique=True, editable=False)
    publish = models.BooleanField(default=False)
    value = RichTextField(max_length=20000, blank=True,
                          help_text="The body of this wiki entry, without custom fields. Displayed above the custom"
                                    " fields in the wiki page.")
    custom_fields_presentation_order = models.ManyToManyField(CustomFieldType, blank=True,
                                                              help_text="Add custom field types 'blocks' to this page."
                                                                        " The presentation order (that is determined by"
                                                                        " the order id of the types) will be shown on"
                                                                        "the right after saving.")
    custom_fields = models.ManyToManyField(CustomField, blank=True,
                                           help_text="Add fields to a 'block' off a custom field type. The presentation"
                                                     " order (that is determined by the order id of the fields) will be"
                                                     " shown on the right after saving.")
    favorite_by = models.ManyToManyField(User, blank=True,
                                         help_text="A list of users that marked this entry as their favorite will be"
                                                   " shown on the right. Use to see how popular an entry is.")
    order_id = models.PositiveSmallIntegerField(default=0, help_text="The presentation order in wiki section page,"
                                                                     " relative to other entries of this type.")

    class Meta:
        ordering = ["section__order_id", "order_id", "slug"]
        verbose_name_plural = "entries"

    def __str__(self):
        return f"[{self.section.name}] {self.name}"

    def save(self, *args, **kwargs):
        # update slug field when saving from admin:
        self.slug = self.section.slug + "-" + slugify(self.name)
        super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("wiki_entry", args=[self.slug])

    def display_favorites(self):
        """
        Used by the admin page to display the number of users that marked this entry as favorite in the entries list
        :return: the number of users
        """
        return len(self.favorite_by.all())

    # this is the title of the admin page column that holds the display_favorites() data
    display_favorites.short_description = "Favorite count"
