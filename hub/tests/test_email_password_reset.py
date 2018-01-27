from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase
from django.urls import reverse


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='testUser', email='test@hub.com', password='12345678')
        self.response = self.client.post(reverse('password_reset'), {'email': 'test@hub.com'})
        self.email = mail.outbox[0]

    def test_email_subject(self):
        self.assertEqual('Please reset your password', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('testUser', self.email.body)

    def test_email_to(self):
        self.assertEqual(['test@hub.com'], self.email.to)
