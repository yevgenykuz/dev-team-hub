from django.test import TestCase
from hub.templatetags.numerical_presnentation_tags import as_percentage


class NumericalPresentationTemplateTagsTests(TestCase):
    def test_numerical_presentation_tags(self):
        expected = "{:.2%}".format(0.486342)
        self.assertEquals(expected, as_percentage(0.486342))