from django.template import Template, Context
from django.test import TestCase
from hub.models import SiteConfig


class SiteConfigTemplateTagsTests(TestCase):
    def setUp(self):
        SiteConfig.objects.create(pk=1)

    def test_site_name_tag(self):
        rendered = Template("{% load site_config_tags %}"
                            "{% site_name request %}").render(Context())
        self.assertEquals(SiteConfig.objects.get(pk=1).name, rendered)

    def test_site_current_release_version_tag(self):
        rendered = Template("{% load site_config_tags %}"
                            "{% site_current_release_version request %}").render(Context())
        self.assertEquals(SiteConfig.objects.get(pk=1).current_release_version, rendered)

    def test_site_current_release_notes_tag(self):
        rendered = Template("{% load site_config_tags %}"
                            "{% site_current_release_notes request %}").render(Context())
        self.assertEquals('None', rendered)

    def test_site_custom_links_tag(self):
        rendered = Template("{% load site_config_tags %}"
                            "{% site_current_release_notes request %}").render(Context())
        self.assertEquals('None', rendered)
