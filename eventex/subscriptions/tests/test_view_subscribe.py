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

    def test_form_context_instance(self):
        """Context must be instance of SubscriptionForm."""
        self.assertIsInstance(self.resp.context['form'], SubscriptionForm)
