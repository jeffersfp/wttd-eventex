from django.core import mail
from django.test import TestCase
from django.conf.global_settings import DEFAULT_FROM_EMAIL


class SubscriptionEmailTest(TestCase):
    def setUp(self):
        data = dict(name='Some Dude', cpf='12345678901',
                    email='somedude@mailinator.com', phone='99999999999')
        self.resp = self.client.post('/inscricao/', data)
        self.email = mail.outbox[0]

    def test_subscription_email_subject(self):
        """Message subject must be 'Eventex - Confirmação de Inscrição'."""
        expect = 'Eventex - Confirmação de inscrição'
        self.assertEqual(self.email.subject, expect)

    def test_subscription_email_from(self):
        """Message sender must be DEFAULT_FROM_EMAIL from settings."""
        expect = DEFAULT_FROM_EMAIL
        self.assertEqual(self.email.from_email, expect)

    def test_subscription_email_to(self):
        expect = [DEFAULT_FROM_EMAIL, 'somedude@mailinator.com']
        self.assertEqual(self.email.to, expect)

    def test_subscription_email_body(self):

        contents = (
            'Some Dude',
            '12345678901',
            'somedude@mailinator.com',
            '99999999999'
        )

        for content in contents:
            with self.subTest():
                self.assertIn(content, self.email.body)
