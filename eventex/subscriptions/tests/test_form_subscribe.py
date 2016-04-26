from django.test import TestCase


class SubscribeFormTest(TestCase):
    def setUp(self):
        self.resp = self.client.get('/inscricao/')

    def test_has_form_elements(self):
        """Page must have all the form elements."""
        tags = (
            ('<form', 1),
            ('<input', 6),
            ('type="text"', 3),
            ('type="email"', 1),
            ('type="submit"', 1)
        )

        for text, count in tags:
            with self.subTest():
                self.assertContains(self.resp, text, count)

    def test_form_has_fields(self):
        """Form must have SubscriptionForm fields."""
        form = self.resp.context['form']
        self.assertSequenceEqual(['name', 'cpf', 'email', 'phone'],
                                 list(form.fields))
