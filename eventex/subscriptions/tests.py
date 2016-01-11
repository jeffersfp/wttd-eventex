from django.test import TestCase
from eventex.subscriptions.forms import SubscriptionForm


class SubscriptionTest(TestCase):
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
        self.assertContains(self.resp, '<form')
        self.assertContains(self.resp, '<input', 6)
        self.assertContains(self.resp, 'type="text"', 3)
        self.assertContains(self.resp, 'type="email"')
        self.assertContains(self.resp, 'type="submit"')

    def test_subscription_form_instance(self):
        self.assertIsInstance(self.resp.context['form'], SubscriptionForm)
