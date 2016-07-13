from django.core import mail
from django.test import TestCase
from django.conf import settings


class SubscribePostValid(TestCase):
    def setUp(self):
        data = dict(name='Henrique Bastos', cpf='12345678901',
                    email='henrique@bastos.net', phone='31-90000-0000')
        self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        expect = 'Eventex - Confirmação de inscrição'
        self.assertEqual(expect, self.email.subject)

    def test_subscription_email_from(self):
        self.assertEqual(settings.DEFAULT_FROM_EMAIL, self.email.from_email)

    def test_subscription_email_to(self):
        expect = [settings.DEFAULT_FROM_EMAIL, 'henrique@bastos.net']
        self.assertEqual(expect, self.email.to)

    def test_subscription_email_body(self):
        contents = [
            'Henrique Bastos',
            '12345678901',
            'henrique@bastos.net',
            '31-90000-0000'
        ]
        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)