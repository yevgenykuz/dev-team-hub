from django.db import models

from news.models import Article


class CustomLink(models.Model):
    name = models.CharField(max_length=50, unique=True)
    order_id = models.PositiveSmallIntegerField(unique=True, default=0,
                                                help_text="Order for custom links drop-down menu")
    url = models.CharField(max_length=255)

    class Meta:
        ordering = ["order_id"]

    def __str__(self):
        return f"[{self.name}]: {self.url}"


class SiteConfig(models.Model):
    name = models.CharField(max_length=50, default="Dev Team Hub")
    current_release_version = models.CharField(max_length=50, default="0.0.1-SNAPSHOT")
    current_release_notes = models.ForeignKey(Article, null=True, on_delete=models.SET_NULL,
                                              help_text="Link to release notes article")
    custom_links = models.ManyToManyField(CustomLink, blank=True, help_text="Choose custom links")

    class Meta:
        verbose_name_plural = "site config"

    def __str__(self):
        return f"[{self.name}]: Current release version: {self.current_release_version}; Custom links: " \
               + self.display_links()

    def display_links(self):
        """
        Used by the admin page to add the links of this site config to the config list
        :return: a string representation of the custom links of this site
        """
        return ", ".join([link.__str__() for link in self.custom_links.all()])

    # this is the title of the admin page column that holds the display_links() data
    display_links.short_description = "Custom Links"
