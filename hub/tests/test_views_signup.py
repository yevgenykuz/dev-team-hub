from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from hub.forms import SignUpForm


class SignupViewStructureTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('signup'))

    def test_view_contains_form(self):
        self.assertIsInstance(self.response.context.get('form'), SignUpForm)

    def test_form_structure(self):
        """
        Form needs to have: csrf, username, email, password1, password2
        """
        self.assertContains(self.response, '<input', 5)
        self.assertContains(self.response, 'type="text"', 1)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)


class SignupViewNewUserTests(TestCase):
    def setUp(self):
        form_data = {
            'username': 'User1',
            'email': 'user1@company.com',
            'password1': '123456abcdefg',
            'password2': '123456abcdefg'
        }
        self.response = self.client.post(reverse('signup'), form_data)
        self.index_url = reverse('index')

    def test_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_view_redirection(self):
        """
        Successful signup should redirect to index page, and new user should be logged in.
        """
        self.assertRedirects(self.response, self.index_url)
        page_after_signup = self.client.get(self.index_url)
        new_user = page_after_signup.context.get('user')
        self.assertTrue(new_user.is_authenticated)


class SignupViewInvalidUserDataTests(TestCase):
    def setUp(self):
        form_data = {}  # empty form
        self.response = self.client.post(reverse('signup'), form_data)

    def test_signup_form_has_errors(self):
        signup_form = self.response.context.get('form')
        self.assertTrue(signup_form.errors)

    def test_no_user_created(self):
        self.assertFalse(User.objects.exists())
