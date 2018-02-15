from django.test import TestCase

from ..models import SiteConfig, CustomLink


class SiteConfigModelTests(TestCase):
    def setUp(self):
        self.site_config = SiteConfig.objects.create()

    def test_new_object_defaults(self):
        self.assertEquals(self.site_config.name, 'Dev Team Hub')
        self.assertEquals(self.site_config.current_release_version, '0.0.1-SNAPSHOT')
        self.assertEquals(self.site_config.current_release_notes, None)

    def test_field_name(self):
        field_label = self.site_config._meta.get_field('name').verbose_name
        max_length = self.site_config._meta.get_field('name').max_length
        self.assertEquals(field_label, 'name')
        self.assertEquals(max_length, 50)

    def test_field_current_release_version(self):
        field_label = self.site_config._meta.get_field('current_release_version').verbose_name
        max_length = self.site_config._meta.get_field('current_release_version').max_length
        self.assertEquals(field_label, 'current release version')
        self.assertEquals(max_length, 50)

    def test_object_presentation(self):
        expected_presentation = f"[{self.site_config.name}]: Current release version: " + \
                                f"{self.site_config.current_release_version}"
        self.assertEquals(expected_presentation, str(self.site_config))

    def test_object_verbose_name_plural(self):
        self.assertEquals(self.site_config._meta.verbose_name_plural, "site config")

    def test_display_links(self):
        custom_link1 = CustomLink.objects.create(name='Google', url='https://www.google.com', order_id=1)
        custom_link2 = CustomLink.objects.create(name='Wikipedia', url='https://en.wikipedia.org', order_id=2)
        self.site_config.custom_links.add(custom_link1)
        self.site_config.custom_links.add(custom_link2)
        expected_presentation = ", ".join([link.__str__() for link in self.site_config.custom_links.all()])
        self.assertEquals(expected_presentation, self.site_config.display_links())

    def test_display_links_short_description(self):
        self.assertEquals(self.site_config.display_links.short_description, "Custom Links")
