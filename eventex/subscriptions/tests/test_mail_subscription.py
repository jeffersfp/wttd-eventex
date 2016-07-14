from django.core import mail
from django.test import TestCase
from django.conf import settings


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Jefferson Pires', cpf='12345678901',
                    email='jeffersfp@mailinator.com', phone='31-90000-0000')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Eventex - Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        self.assertEqual(settings.DEFAULT_FROM_EMAIL, self.email.from_email)

    def test_subscription_email_to(self):
        expect = [settings.DEFAULT_FROM_EMAIL, 'jeffersfp@mailinator.com']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Jefferson Pires',
            '12345678901',
            'jeffersfp@mailinator.com',
            '31-90000-0000'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)