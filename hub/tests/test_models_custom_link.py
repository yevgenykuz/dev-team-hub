from django.test import TestCase

from ..models import CustomLink


class CustomLinkModelTests(TestCase):
    def setUp(self):
        CustomLink.objects.create(name='Google', url='https://www.google.com', order_id=1)
        self.custom_link = CustomLink.objects.get(name='Google', url='https://www.google.com', order_id=1)

    def test_field_name(self):
        field_label = self.custom_link._meta.get_field('name').verbose_name
        max_length = self.custom_link._meta.get_field('name').max_length
        unique = self.custom_link._meta.get_field('name').unique
        self.assertEquals(field_label, 'name')
        self.assertEquals(max_length, 50)
        self.assertEquals(unique, True)

    def test_field_url(self):
        field_label = self.custom_link._meta.get_field('url').verbose_name
        max_length = self.custom_link._meta.get_field('url').max_length
        self.assertEquals(field_label, 'url')
        self.assertEquals(max_length, 255)

    def test_field_order_id(self):
        field_label = self.custom_link._meta.get_field('order_id').verbose_name
        max_length = self.custom_link._meta.get_field('order_id').default
        self.assertEquals(field_label, 'order id')
        self.assertEquals(max_length, 0)

    def test_object_presentation(self):
        expected_presentation = f"[{self.custom_link.name}]: {self.custom_link.url}"
        self.assertEquals(expected_presentation, str(self.custom_link))

    def test_object_ordering(self):
        self.assertEquals(self.custom_link._meta.ordering, ['order_id'])

    def test_new_object(self):
        self.assertEquals(self.custom_link.name, 'Google')
        self.assertEquals(self.custom_link.url, 'https://www.google.com')
        self.assertEquals(self.custom_link.order_id, 1)
