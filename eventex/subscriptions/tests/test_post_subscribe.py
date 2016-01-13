from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionPostTest(TestCase):
    def setUp(self):
        data = dict(name='Some Dude', cpf='99999999999',
                    email='somedude@mailinator.com', phone='99999999999')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid post should redirect to /inscricao/ with status code 302."""
        self.assertEqual(self.resp.status_code, 302)

    def test_subscribe_send_email(self):
        """Mail must have 1 message in its outbox."""
        self.assertEqual(len(mail.outbox), 1)


class SubscriptionPostInvalidTest(TestCase):
    def setUp(self):
        self.resp = self.client.post('/inscricao/', {})

    def test_post(self):
        """Invalid POST should not redirect"""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        """Should use template subscription_form.html"""
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_form.html')

    def test_form(self):
        form = self.resp.context['form']
        self.assertIsInstance(form, SubscriptionForm)

    def test_form_has_errors(self):
        form = self.resp.context['form']
        self.assertTrue(form.errors)


class SubscriptionSuccessTest(TestCase):
    def test_success(self):
        data = dict(name='Some Dude',
                    cpf='99999999999',
                    email='somedude@mailinator.com',
                    phone='99999999999')
        resp = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(resp, 'Inscrição realizada com sucesso!')
