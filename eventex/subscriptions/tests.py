from django.core import mail
from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionGetTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_get(self):
        """GET /inscricao/ must return status code 200."""
        self.assertEqual(self.resp.status_code, 200)

    def test_template(self):
        """Must use subscription_form.html template."""
        self.assertTemplateUsed(self.resp,
                                'subscriptions/subscription_form.html')

    def test_has_form_elements(self):
        """Page must have all the form elements."""
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_form_context_instance(self):
        """Context must be instance of SubscriptionForm."""
        self.assertIsInstance(self.resp.context['form'], SubscriptionForm)

    def test_form_has_fields(self):
        """Form must have SubscriptionForm fields."""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'],
                                 list(form.fields))


class SubscriptionPostTest(TestCase):
    def setUp(self):
        data = dict(name='Jefferson Pires', cpf='12345678901',
                    email='jeffersfp@gmail.com', phone='19988442075')
        self.resp = self.client.post('/inscricao/', data)

    def test_post(self):
        """Valid post should redirect to /inscricao/ with status code 302."""
        self.assertEqual(self.resp.status_code, 302)

    def test_subscribe_send_email(self):
        """Mail must have 1 message in its outbox."""
        self.assertEqual(len(mail.outbox), 1)

    def test_subscription_email_subject(self):
        """Message subject must be 'Eventex - Confirmação de Inscrição'."""
        email = mail.outbox[0]
        expect = 'Eventex - Confirmação de inscrição'

        self.assertEqual(email.subject, expect)

    def test_subscription_email_from(self):
        """Message sender must be 'contato@eventex.com.br"""
        email = mail.outbox[0]
        expect = 'contato@eventex.com.br'

        self.assertEqual(email.from_email, expect)

    def test_subscription_email_to(self):
        email = mail.outbox[0]
        expect = ['contato@eventex.com.br', 'jeffersfp@gmail.com']

        self.assertEqual(email.to, expect)

    def test_subscription_email_body(self):
        email = mail.outbox[0]

        self.assertIn('Jefferson Pires', email.body)
        self.assertIn('12345678901', email.body)
        self.assertIn('jeffersfp@gmail.com', email.body)
        self.assertIn('19988442075', email.body)


class SubscriptionInvalidPostTest(TestCase):
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
        data = dict(name='Jefferson Pires', cpf='1298309128',
                    email='jeffersfp@mailinator.com', phone='19829712333')
        resp = self.client.post('/inscricao/', data, follow=True)
        self.assertContains(resp, 'Inscrição realizada com sucesso!')